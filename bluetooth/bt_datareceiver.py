import asyncio
from bleak import BleakScanner, BleakClient
import struct
import mysql.connector
from mysql.connector import errorcode

# Database connection setup
try:
    cnx = mysql.connector.connect(user='dbaccess_rw', password='fasdjkf2389vw2c3k234vk2f3',
                                  host='172.20.241.9',
                                  database='measurements')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    print("Connected to the database")
    cursor = cnx.cursor()

groupid = 10

direction_values = []
x_values = []
y_values = []
z_values = []

insert_data = ("INSERT INTO rawdata "
               "(groupid, sensorvalue_a, sensorvalue_b, sensorvalue_c, sensorvalue_d)"
               "VALUES (%s, %s, %s, %s, %s)")

# Replace with your device's name and characteristic UUID
device_name = "paivarintakokko"
characteristic_uuid = "00001526-1212-efde-1523-785feabcd123"

async def discover_device(device_name):
    devices = await BleakScanner.discover()
    for device in devices:
        if device_name and device.name and device_name in device.name:
            return device.address
    return None

async def connect_and_subscribe(device_address, characteristic_uuid):
    counter = [0]  # Counter to track the number of insertions
    direction_values = []
    x_values = []
    y_values = []
    z_values = []

    async def notification_handler(sender: int, data: bytearray):
        nonlocal direction_values, x_values, y_values, z_values, counter
        global i 
        decoded_value = struct.unpack('<i', data)[0]
        print(f"Decimal value: {decoded_value}")

        if decoded_value <= 5 and decoded_value > 0:
            i = 0
        else:
            i = (i + 1) % 4

        if i == 0:
            direction_values.append(decoded_value)
        elif i == 1:
            x_values.append(decoded_value)
        elif i == 2:
            y_values.append(decoded_value)
        elif i == 3:
            z_values.append(decoded_value)

        counter[0] += 1  # Increment the counter

        if counter[0] >= 10:
            # Stop further data insertion
            notify_task.cancel()

    async with BleakClient(device_address) as client:
        # Find the characteristic by UUID
        services = await client.get_services()

        for service in services:
            characteristics = service.characteristics
            for char in characteristics:
                if char.uuid.lower() == characteristic_uuid.lower():
                    target_characteristic = char
                    break

        notify_task = asyncio.ensure_future(client.start_notify(target_characteristic.handle, notification_handler))
        await asyncio.sleep(30)  # Listen for notifications for 30 seconds

    # Iterate over the lists and insert data
    for i in range(len(direction_values)):
        data = (groupid, direction_values[i], x_values[i], y_values[i], z_values[i])

        try:
            # Execute the query
            cursor.execute(insert_data, data)

            # Commit the changes to the database
            cnx.commit()

        except mysql.connector.Error as err:
            # Handle any errors that occur during the insertion
            print(f"Error: {err}")
            cnx.rollback()

    # Close the cursor
    cursor.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    device_address = loop.run_until_complete(discover_device(device_name))
    if device_address:
        print(f"Found device at {device_address}")
        try:
            loop.run_until_complete(connect_and_subscribe(device_address, characteristic_uuid))
        except asyncio.CancelledError:
            print("Data insertion stopped.")
    else:
        print(f"Device '{device_name}' not found.")
    cnx.close()
