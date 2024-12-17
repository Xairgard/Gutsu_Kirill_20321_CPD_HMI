## Задание
Разобрать пример с GitHub
Добавить свою функцию

## Листинг 
### Server
``` py
from concurrent import futures
import time
from typing import OrderedDict
import uuid
from google.protobuf import wrappers_pb2

import grpc
import order_management_pb2_grpc
import order_management_pb2


class OrderManagementServicer(order_management_pb2_grpc.OrderManagementServicer):

    def __init__(self):
        self.orderDict = {}
        # Заполнение словаря образцами заказов
        self.orderDict['101'] = order_management_pb2.Order(id='101', price=1000,
                                                           items=['Item - A', 'Item - B'],
                                                           description='Sample order description.')
        self.orderDict['102'] = order_management_pb2.Order(id='102', price=1000,
                                                           items=['Item - C'],
                                                           description='Sample order description.')
        self.orderDict['103'] = order_management_pb2.Order(id='103', price=1000,
                                                           items=['Item - A', 'Item - E'],
                                                           description='Sample order description.')
        self.orderDict['104'] = order_management_pb2.Order(id='104', price=1000,
                                                           items=['Item - F', 'Item - G'],
                                                           description='Sample order description.')

        # Unary RPC

    def getOrder(self, request, context):
        # Поиск заказа по идентификатору
        order = self.orderDict.get(request.value)
        if order is not None:
            return order
        else:
            # Обработка ошибки при неудачном поиске
            print('Order not found ' + request.value)
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Order : ', request.value, ' Not Found.')
            return order_management_pb2.Order()

    # Unary RPC
    def addOrder(self, request, context):
        # Генерация id
        id = uuid.uuid1()
        request.id = str(id)
        # Добавление заказа в словарь
        self.orderDict[request.id] = request
        response = wrappers_pb2.StringValue(value=str(id))
        print(self.orderDict)
        return response

    # Server Streaming
    def searchOrders(self, request, context):
        # Поиск заказов
        matching_orders = self.searchInventory(request.value)
        #  Отправляем найденный заказ в поток.
        for order in matching_orders:
            yield order

    # Client Streaming
    def updateOrders(self, request_iterator, context):
        # Обновление информации про заказ
        response = 'Updated IDs :'
        for order in request_iterator:
            self.orderDict[order.id] = order
            response += ' ' + order.id
        return wrappers_pb2.StringValue(value=response)

    # Bi-di Streaming
    def processOrders(self, request_iterator, context):
        # Принамаем поток индефикаторов и возращаем CombinedShipment
        print('Processing orders.. ')
        shipment_id = uuid.uuid1()
        shipments = []

        shipment = order_management_pb2.CombinedShipment(id=str(shipment_id), status='PROCESSED', )
        shipments.append(shipment)
        for order_id in request_iterator:
            for order in shipments:
                yield order

    # Local function
    def searchInventory(self, query):
        # Поиск ордера
        matchingOrders = []
        for order_id, order in self.orderDict.items():
            for itm in order.items:
                if query in itm:
                    matchingOrders.append(order)
                    break
        return matchingOrders


# Creating gRPC Server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
order_management_pb2_grpc.add_OrderManagementServicer_to_server(OrderManagementServicer(), server)
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()

```
### Client
``` py
from google.protobuf import wrappers_pb2
import grpc
import order_management_pb2
import order_management_pb2_grpc

import time

# Функция для запуска клиента
def run():
    # Устанавливаем соединение с gRPC сервером
    channel = grpc.insecure_channel('localhost:50051')

    # Cоздайте заглушку
    stub = order_management_pb2_grpc.OrderManagementStub(channel)

    # Создание заказа
    order1 = order_management_pb2.Order(items=['Item - A', 'Item - B', 'Item - C'],
                                        price=2450.50,
                                        description='This is a Sample order - 1 : description.',
                                        destination='San Jose, CA')

    # Получение заказа по его идентификатору
    order = stub.getOrder(order_management_pb2.Order(id='101'))
    print("Order service response", order)

    # Добавление нового заказа
    response = stub.addOrder(order1)
    print('Add order response :', response)

    # Поиск заказов
    for order_search_result in stub.searchOrders(wrappers_pb2.StringValue(value='Item - A')):
        print('Search Result : ', order_search_result)

    # обновление заказов
    upd_order_iterator = generate_orders_for_updates()
    upd_status = stub.updateOrders(upd_order_iterator)
    print('Order update status : ', upd_status)

    # Вызываем удаленный метод и получаем ссылку на поток для записи и чтения на клиентской стороне.
    proc_order_iterator = generate_orders_for_processing()
    for shipment in stub.processOrders(proc_order_iterator):
        print(shipment)


def generate_orders_for_updates():
    # Создание нескольких обновленных заказов
    ord1 = order_management_pb2.Order(id='101', price=1000,
                                      items=['Item - A', 'Item - B', 'Item - C', 'Item - D'],
                                      description='Sample order description.',
                                      destination='Mountain View, CA')
    ord2 = order_management_pb2.Order(id='102', price=1000,
                                      items=['Item - E', 'Item - Q', 'Item - R', 'Item - D'],
                                      description='Sample order description.',
                                      destination='San Jose, CA')
    ord3 = order_management_pb2.Order(id='103', price=1000,
                                      items=['Item - A', 'Item - K'],
                                      description='Sample order description.',
                                      destination='San Francisco, CA')
    list = []
    list.append(ord1)
    list.append(ord2)
    list.append(ord3)

    for updated_orders in list:
        yield updated_orders


def generate_orders_for_processing():
    # Создание заказов для обработки
    ord1 = order_management_pb2.Order(
        id='104', price=2332,
        items=['Item - A', 'Item - B'],
        description='Updated desc',
        destination='San Jose, CA')
    ord2 = order_management_pb2.Order(
        id='105', price=3000,
        description='Updated desc',
        destination='San Francisco, CA')
    ord3 = order_management_pb2.Order(
        id='106', price=2560,
        description='Updated desc',
        destination='San Francisco, CA')
    ord4 = order_management_pb2.Order(
        id='107', price=2560,
        description='Updated desc',
        destination='Mountain View, CA')
    list = []
    list.append(ord1)
    list.append(ord1)
    list.append(ord3)
    list.append(ord4)

    for processing_orders in list:
        yield processing_orders


run()
```

## Скриншот
# Server
![alt text](https://github.com/Xairgard/Gutsu_Kirill_20321_CPD_HMI/blob/main/CPD/Task_6/png/Server.png)
# Client
![alt text](https://github.com/Xairgard/Gutsu_Kirill_20321_CPD_HMI/blob/main/CPD/Task_6/png/Client_1.png)
![alt text](https://github.com/Xairgard/Gutsu_Kirill_20321_CPD_HMI/blob/main/CPD/Task_6/png/Client_2.png)
