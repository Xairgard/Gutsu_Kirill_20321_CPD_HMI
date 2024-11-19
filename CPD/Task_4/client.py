import cv2
import socket
import product_info_pb2

# Инициализация proto
image_proto = product_info_pb2.my_image()

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
