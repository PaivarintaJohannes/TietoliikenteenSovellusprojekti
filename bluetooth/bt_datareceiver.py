import asyncio
from bleak import BleakScanner, BleakClient
import struct

direction_value = []
x_values = []
y_values = []
z_values = []

# Replace with your device's name and characteristic UUID
device_name = "MY_LBS2"
characteristic_uuid = "00001526-1212-efde-1523-785feabcd123"

async def discover_device(device_name):
    devices = await BleakScanner.discover()
    for device in devices:
        if device_name and device.name and device_name in device.name:
            return device.address
    return None

async def connect_and_subscribe(device_address, characteristic_uuid):
    async with BleakClient(device_address) as client:
        # Find the characteristic by UUID
        services = await client.get_services()

        for service in services:
            characteristics = service.characteristics
            for char in characteristics:
                if char.uuid.lower() == characteristic_uuid.lower():
                    target_characteristic = char
                    break

        def notification_handler(data: bytearray):            
            global i

            decoded_value = struct.unpack('<i', data)[0]
            print(f"Decimal value: {decoded_value}")

            if decoded_value <= 5 and decoded_value > 0:
                i = 0
            else:
                i = (i + 1) % 4

            if i == 0:
                direction_value.append(decoded_value)  
            elif i == 1:
                x_values.append(decoded_value) 
            elif i == 2:
                y_values.append(decoded_value) 
            elif i == 3:
                z_values.append(decoded_value)
                

        await client.start_notify(target_characteristic.handle, notification_handler)
        await asyncio.sleep(30)  # Listen for notifications for 30 seconds

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    device_address = loop.run_until_complete(discover_device(device_name))
    if device_address:
        print(f"Found device at {device_address}")
        loop.run_until_complete(connect_and_subscribe(device_address, characteristic_uuid))
    else:
        print(f"Device '{device_name}' not found.")
