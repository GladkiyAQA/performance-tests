from pydantic import BaseModel


class GRPCClientConfig(BaseModel):
    # Порт gRPC-сервиса, к которому подключаемся (например, 9003)
    port: int

    # Хост (например, localhost или grpc-gateway.internal)
    host: str

    @property
    def client_url(self) -> str:
        """
        Возвращает адрес подключения в формате host:port,
        который требуется для создания gRPC-канала через insecure_channel().
        """
        return f"{self.host}:{self.port}"
