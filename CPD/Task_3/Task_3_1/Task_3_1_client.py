import socket

import time

sock = socket.socket()
SERVER_IP = 'localhost'
SERVER_PORT = 12345

sock.connect((SERVER_IP, SERVER_PORT))

while True:
    try:
        data_enc = "encode"

        time.sleep(1)
        sock.send(data_enc.encode())

    except KeyboardInterrupt:
        break

sock.close()