from locust import User, between, task

from clients.grpc.gateway.users.client import UsersGatewayGRPCClient, build_users_gateway_locust_grpc_client
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse


class GetUserScenarioUser(User):
    # Атрибут host обязателен для Locust, даже если он не используется напрямую в gRPC.
    host = "localhost"
    # Время ожидания между задачами от 1 до 3 секунд.
    wait_time = between(1, 3)

    # Аннотации для клиентов и ответов
    users_gateway_client: UsersGatewayGRPCClient
    create_user_response: CreateUserResponse

    def on_start(self) -> None:
        """
        Метод, вызываемый при старте каждого виртуального пользователя.
        Здесь происходит инициализация gRPC API клиента и создание пользователя.
        """
        # Инициализируем gRPC-клиент, пригодный для Locust, с интерцептором метрик.
        self.users_gateway_client = build_users_gateway_locust_grpc_client(self.environment)

        # Создаём пользователя один раз в начале сессии.
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def get_user(self):
        """
        Основная задача виртуального пользователя — получение данных пользователя.
        Метод будет многократно вызываться Locust-агентами.
        """
        self.users_gateway_client.get_user(self.create_user_response.user.id)
