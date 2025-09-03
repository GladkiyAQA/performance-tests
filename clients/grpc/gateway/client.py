from grpc import Channel, insecure_channel


def build_gateway_grpc_client() -> Channel:
    """
    Фабричная функция (билдер) для создания gRPC-канала к сервису grpc-gateway.

    :return: gRPC-канал (Channel), настроенный на адрес localhost:9003.
    """
    # Создаём небезопасное (без TLS) соединение с gRPC-сервером по адресу localhost:9003
    return insecure_channel("localhost:9003")

