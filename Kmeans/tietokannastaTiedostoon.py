#!/usr/bin/python3

# pip install pySerial # Asenna tämä ellei ole asennettu
from code import interact
import numpy as np
import sys
import csv


#pip install mysql-connector-python  # Asenna tuo ellei ole jo asennettu.
from getpass import getpass
from mysql.connector import connect, Error
from datetime import datetime

# tarkistetaan, että käyttäjä antaa 2 parametria groupID:n ja tiedostonimen
N = len(sys.argv)
#print("Annoit ", N , "kpl parametreja")
if(N<3):
    print("Anna groupId ja tiedostonimi parametreina")
    sys.exit()

groupID = sys.argv[1]
fileName = sys.argv[2]
print("Annoit groupID = ", groupID)
print("Annoit tiedoston nimeksi = ", fileName)

query = """
SELECT sensorvalue_a, sensorvalue_b, sensorvalue_c,sensorvalue_e from rawdata where groupid = """
query = query + str(groupID)


try:
    with connect(
        host="172.20.241.9",
        user="dbaccess_rw",
        password="fasdjkf2389vw2c3k234vk2f3",
        database="measurements",
    ) as connection:
    #print(connection)
        with connection.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            #print(records)
            cursor.close()
        connection.close()
except Error as e:
    print(e)

print("records length = ", len(records))

# Luetaan tietokannasta siis vain x,y,z ja label = orientaatiotieto
# laitetaan luetut numpy matriisiin
nbrOfMeas = len(records)
if(nbrOfMeas<1):
    print("Ei löytynyt dataa tietokannasta tällä groupID:llä")
    sys.exit()
data = np.zeros((nbrOfMeas,4),dtype=np.float32)
data[:,:] = records[:][:]


# Ja lopuksi kirjoitetaan tietokannasta luettu data tiedostoon.
#with open(fileName, 'w', encoding='UTF8', newline='') as f:
with open(fileName, 'w', newline='') as f:
    writer = csv.writer(f)
    for i in range(nbrOfMeas):
        #f.write(str(data[i,:]))  # kirjoitetaan rivi kerrallaan matriisista
        #f.write(str(records[i][:]))
        writer.writerow(data[i,:])

    f.close()




