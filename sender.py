"""
Client that sends the file (uploads)
"""

import tqdm
import socket
import os

SEPARATOR = '<SEP>'
BUFFER_SIZE = 4096

# the ip address or hostname of the server, the receiver
host = '192.168.31.166'  # kali linux ip
port = 8080

filename = 'data.txt'
filesize = os.path.getsize(filename)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f'[+] Connecting to {host}:{port}')
s.connect((host, port))
print(f'[+] Connected.')

s.send(f'{filename}{SEPARATOR}{filesize}'.encode())

# start sending the file
progress = tqdm.tqdm(range(filesize), f'Sending {filename}', unit='B', unit_scale=True, unit_divisor=1024)


with open(filename, 'rb') as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)

        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transmission in
        # busy networks
        s.sendall(bytes_read)

        progress.update(len(bytes_read))

s.close()
