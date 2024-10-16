import socket
import os
import tqdm

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

BUFFER_SIZE = 4096
SEPARATOR = '<SEP>'

s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, addr = s.accept()

print(f"[+] {addr} is connected.")

received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)

filename = os.path.basename(filename)

filesize = int(filesize)


# start receiving the file from the socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f'Receiving {filename}', unit='B', unit_scale=True, unit_divisor=1024)

with open(filename, 'wb') as f:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)

        if not bytes_read:
            # nothing is received
            # file transmitting is done
            break

        f.write(bytes_read)

        progress.update(len(bytes_read))

client_socket.close()
s.close()
