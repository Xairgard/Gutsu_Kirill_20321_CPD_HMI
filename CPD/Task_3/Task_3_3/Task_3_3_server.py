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
