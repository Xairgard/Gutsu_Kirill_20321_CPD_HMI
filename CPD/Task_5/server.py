from concurrent import futures
import logging
import uuid
import grpc
import time

import product_info_pb2
import product_info_pb2_grpc

class ProductInfoServicer(product_info_pb2_grpc.ProductInfoServicer):
    def init(self):
        self.productMap = {}

    def addProduct(self, request, context):
        # Генерация id
        id = str(uuid.uuid1())
        request.id = id
        print("addProduct:request", request)
        # Добавление информации в словарь
        self.productMap[id] = request
        response = product_info_pb2.ProductID(value=id)
        print("addProduct:response", response)
        return response

    def getProduct(self, request, context):
        print("getProduct:request", request)
        # Получение информации по id
        id = request.value
        response = self.productMap[id]
        print("getProduct:response", response)
        return response

    def delProduct(self, request, context):
        print("delProduct:request", request)
        # Удаление информации по id
        id = request.id
        if id in self.productMap:
            del self.productMap[id]
            response = product_info_pb2.DeleteResponse(success=True)
        else:
            response = product_info_pb2.DeleteResponse(success=False)
        print("delProduct:response", response)
        return response

# Создание gRPC-сервера
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
# Использование сгенерированную функцию `add_Calculator Services_to_server`, чтобы добавить определенный класс на сервер
product_info_pb2_grpc.add_ProductInfoServicer_to_server(ProductInfoServicer(), server)

# Gрослушивание на порту 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
# Запуск сервера
server.start()

# Запуск бесконечного цикла для продолжения работы сервера
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    # Остановка сервера при получении сигнала прерывания
    server.stop(0)
