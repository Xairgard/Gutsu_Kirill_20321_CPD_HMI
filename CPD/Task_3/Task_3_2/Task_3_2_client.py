import socket
import pickle

import time

sock = socket.socket()
SERVER_IP = 'localhost'
SERVER_PORT = 12345

sock.connect((SERVER_IP, SERVER_PORT))

while True:
    try:
        data_pick = 'pickle'

        time.sleep(1)
        sock.send(pickle.dumps(data_pick, pickle.HIGHEST_PROTOCOL))
    except KeyboardInterrupt:
        break

sock.close()