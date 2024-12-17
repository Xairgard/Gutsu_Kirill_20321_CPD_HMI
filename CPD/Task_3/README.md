TCP Client-streaming (Клиент, например, раз в 1 секунду отправляет данные на сервер), используя встроенный в Python модуль socket.
# Task_3_1
Используя encode() и decode()

## Task_3_1_server.py листинг
```Py
import socket

sock = socket.socket()
sock.bind(('localhost', 12345))

sock.listen(1)
print("Сервер запущен и ожидает подключения...")
conn, addr = sock.accept()
print("Подключение от", addr)
while True:
    data = conn.recv(1024)
    if not data:
        break
    
    print(data.decode())

conn.close()
```
## Task_3_1_client.py листинг
```Py
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
```
## Пояснение и скриншоты результатов работы
Task_3_1_server.py Task_3_1_client.py мы используем encode и decode для того что бы передать информацию на сервер и принять её сервером

![alt text](https://github.com/Xairgard/Gutsu_Kirill_20321_CPD_HMI/blob/main/CPD/Task_3/Task_3_1/Task_3_1_server.png)

# Task_3_2
Используя pickle - де/сериализация произвольных объектов.

## Task_3_2_server.py листинг
```Py
import socket
import pickle

sock = socket.socket()
sock.bind(('localhost', 12345))

sock.listen(1)
print("Сервер запущен и ожидает подключения...")
conn, addr = sock.accept()
print("Подключение от", addr)
while True:
    data = conn.recv(1024)
    if not data:
        break
    
    print(pickle.loads(data))

conn.close()
```

## Task_3_2_client.py листинг
```Py
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
```

## Пояснение и скриншоты результатов работы
Task_3_2_server.py Task_3_2_client.py мы используем pickle для де/сериализация произвольных объектов

![alt text](https://github.com/Xairgard/Gutsu_Kirill_20321_CPD_HMI/blob/main/CPD/Task_3/Task_3_2/Task_3_2.png)

# Task_3_3
Используя Google Protocol Buffers - де/сериализация определенных структурированных данных, а не произвольных объектов Python

## Task_3_3_server.py листинг
```Py
import protolc_pb2 as pb
import socket

sock = socket.socket()
sock.bind(('localhost', 12345))
temp = pb.TempEvent()
sock.listen(1)
print("Сервер запущен и ожидает подключения...")
conn, addr = sock.accept()
print("Подключение от", addr)
flag = 0
while True:
    data = conn.recv(1024)
    temp.ParseFromString(data)
    print(temp.device_id)
    print(temp.event_id)
    print(temp.humidity)
    print(temp.temp_cel)

conn.close()
```
## Task_3_3_client.py листинг
```Py
import socket
import pickle
import protolc_pb2
import time

tempev = protolc_pb2.TempEvent()
tempev.device_id = 1234
tempev.event_id = 4321
tempev.humidity = 2.6
tempev.temp_cel = 3.1415

a = tempev.SerializeToString()

sock = socket.socket()
SERVER_IP = 'localhost'
SERVER_PORT = 12345

sock.connect((SERVER_IP, SERVER_PORT))

while True:
    try:

        time.sleep(1)
        sock.send(a)
        
    except KeyboardInterrupt:
        break

sock.close()
```

## Пояснение и скриншоты результатов работы
Task_3_3_server.py Task_3_3_client.py мы используем Google Protocol Buffers - де/сериализация определенных структурированных данных, а не произвольных объектов Python. Для этого мы создаём файл protolc_pb2, в который записываем типы сообщений

![alt text](https://github.com/Xairgard/Gutsu_Kirill_20321_CPD_HMI/blob/main/CPD/Task_3/Task_3_3/Task_3_3.png)
