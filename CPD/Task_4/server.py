from PySide6.QtCore import QUrl, QByteArray, QTimer
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtNetwork import QTcpServer, QTcpSocket
from PySide6.QtWidgets import QApplication, QMainWindow
import os


class VideoServer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Video Server")

        # Настройка виджета для видео
        self.video_widget = QVideoWidget()
        self.setCentralWidget(self.video_widget)

        # Настройка QMediaPlayer
        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)

        # Логирование ошибок
        self.media_player.errorOccurred.connect(self.on_error)
        self.media_player.mediaStatusChanged.connect(self.on_media_status)

        # Настройка TCP-сервера
        self.tcp_server = QTcpServer(self)
        if not self.tcp_server.listen(port=12345):
            print(f"Не удалось запустить сервер: {self.tcp_server.errorString()}")
            return

        print("Сервер запущен на порту 12345")
        self.tcp_server.newConnection.connect(self.handle_new_connection)

        self.client_socket = None
        self.buffer = QByteArray()

    def handle_new_connection(self):
        self.client_socket = self.tcp_server.nextPendingConnection()
        self.client_socket.readyRead.connect(self.read_data)
        self.client_socket.disconnected.connect(self.client_socket.deleteLater)
        print("Клиент подключен")

    def read_data(self):
        while self.client_socket.bytesAvailable():
            self.buffer.append(self.client_socket.readAll())

        # Если передача завершена, сохраняем данные в видеофайл
        if b'EOF' in self.buffer.data():
            print("Передача завершена")
            self.buffer.remove(self.buffer.indexOf(b'EOF'), 3)  # Удаляем маркер EOF
            video_file = "received_video.mp4"
            with open(video_file, 'wb') as f:
                f.write(self.buffer)
            self.buffer.clear()
            print(f"Видео сохранено как {video_file}")

            # Проверяем размер файла
            file_size = os.path.getsize(video_file)
            print(f"Размер файла: {file_size} байт")

            # Воспроизводим видео
            self.media_player.setSource(QUrl.fromLocalFile(video_file))
            self.media_player.play()

    def on_error(self, error):
        print(f"Ошибка воспроизведения: {error}, {self.media_player.errorString()}")

    def on_media_status(self, status):
        print(f"Статус медиа: {status}")


if __name__ == "__main__":
    app = QApplication([])
    server = VideoServer()
    server.show()
    app.exec()