## Задание
Клиент отправляет видео на PySide6 сервер, где проиходит отображение этого видео в виджете.
PySide6 server - QTcpServer

## Листинг
### Server
```Py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtNetwork import QTcpServer
from PySide6.QtGui import QPixmap
import temp_pb2
import io

class VideoServer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Основное окно
        self.video_label = QLabel()
        self.setCentralWidget(self.video_label)

        # Настройка сервера
        self.tcp_server = QTcpServer(self)
        self.buffer = io.BytesIO()
        self.video_data = temp_pb2.my_image()
        self.tcp_server.newConnection.connect(self.client_conn)
        self.tcp_server.listen(port=12345)

    def client_conn(self):
        # Обработчик нового подключения клиента
        client_socket = self.tcp_server.nextPendingConnection()
        print(client_socket)
        client_socket.readyRead.connect(self.video_tr)

    def video_tr(self):
        # Обработчик готовности данных для чтения
        client_socket = self.sender()

        # Чтение данных видео
        self.buffer.write(client_socket.readAll())
        data_size = len(self.buffer.getvalue())

        # Обработка завершения чтения
        if data_size >= 4:
            # Получение размера сообщения из первых 4 байт
            message_size = int.from_bytes(self.buffer.getvalue()[:4], 'big')
            if data_size >= 4 + message_size:
                # Извлечение данных видео и их обработка
                self.video_data.ParseFromString(self.buffer.getvalue()[4:4 + message_size])
                pixmap = QPixmap()
                pixmap.loadFromData(self.video_data.image)
                self.video_label.setPixmap(pixmap)

                # Обрезаем буфер после успешной обработки сообщения
                self.buffer = io.BytesIO(self.buffer.getvalue()[4 + message_size:])

def main():
    # Основная функция приложения
    app = QApplication([])
    video_server = VideoServer()
    video_server.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

```
### Client
``` py
import cv2
import socket
import temp_pb2

# Инициализация proto
image_proto = temp_pb2.my_image()

# Открытие видео с веб-камеры
video_capture = cv2.VideoCapture(0)

# Настройки сервера
host = '127.0.0.1'
port = 12345

# Подключение к серверу
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.connect((host, port))

    # Отправка видео
    while True:
        ret, frame = video_capture.read()
        ret, buffer = cv2.imencode('.jpg', frame)

        # Сериализация proto
        image_proto.image = bytes(buffer)
        serialized_data = image_proto.SerializeToString()

        # Формирование сообщения с длиной и отправка
        message = len(serialized_data).to_bytes(4, byteorder='big') + serialized_data
        server_socket.sendall(message)

# Закрытие видеопотока
video_capture.release()

```
