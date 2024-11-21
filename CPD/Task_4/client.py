import sys
from PySide6.QtNetwork import QTcpSocket
from PySide6.QtCore import QIODevice, QByteArray


def send_video():
    file_path = "C:\\Users\\kiril\\Desktop\\sssss\\3.mp4"
    host = "localhost"
    port = 12345

    socket = QTcpSocket()
    socket.connectToHost(host, port)

    if not socket.waitForConnected(5000):
        print("Не удалось подключиться к серверу")
        return

    print("Подключено к серверу")

    # Чтение файла и отправка его содержимого
    try:
        with open(file_path, "rb") as f:
            buffer = QByteArray(f.read())  # Читаем весь файл сразу
            socket.write(buffer)  # Отправляем содержимое файла
            socket.waitForBytesWritten(5000)

        # Добавляем маркер окончания передачи
        socket.write(b'EOF')
        socket.waitForBytesWritten(5000)
        print("Видео отправлено")
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        socket.close()

if __name__ == "__main__":
    send_video()