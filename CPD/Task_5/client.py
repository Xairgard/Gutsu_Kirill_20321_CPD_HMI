import grpc
import product_info_pb2
import product_info_pb2_grpc

def run():
    # Установка соединения с сервером
    channel = grpc.insecure_channel('localhost:50051')
    # Cоздайте заглушку
    stub = product_info_pb2_grpc.ProductInfoStub(channel)

    # Создание нового продукта и добавление 
    new_product = product_info_pb2.Product(name="Apple iPhone 11", description="Meet Apple iPhone 11. All-new dual-camera system with Ultra Wide and Night mode.", price=699.0)
    response = stub.addProduct(new_product)
    print("add product: response", response)

    # Получение информации по id
    product_id = response.value
    productInfo = stub.getProduct(product_info_pb2.ProductID(value=product_id))
    print("get product: response", productInfo)

    # Удаление по id
    deleteResponse = stub.delProduct(product_info_pb2.ProductDel(id=product_id))
    print("delete product: response", deleteResponse)

# Запуске скрипта
if __name__ == '__main__':
    run()
