import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('172.20.241.9', 20000))
s.sendall(b'10\n')

chunks = []
while True:
    data = s.recv(1024)
    if len(data) == 0:
        break
    chunks.append(data.decode('utf-8'))

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the file name
file_name = 'received_data.txt'

# Create the file path in the script directory
file_path = os.path.join(script_directory, file_name)

# Write the received data to a file (create the file if it doesn't exist)
with open(file_path, 'w') as file:
    for i in chunks:
        file.write(i)

# Close the file and socket connection
s.close()
