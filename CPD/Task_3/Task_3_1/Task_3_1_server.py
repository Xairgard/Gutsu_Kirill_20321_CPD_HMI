
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
