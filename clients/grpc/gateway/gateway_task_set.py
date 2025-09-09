from locust import TaskSet, SequentialTaskSet

# Импортируем типы и билдеры для построения HTTP API клиентов
from clients.grpc.gateway.accounts.client import AccountsGatewayGRPCClient, build_accounts_gateway_locust_grpc_client
from clients.grpc.gateway.cards.client import CardsGatewayGRPCClient, build_cards_gateway_locust_grpc_client
from clients.grpc.gateway.documents.client import (
    DocumentsGatewayGRPCClient,
    build_documents_gateway_locust_grpc_client
)
from clients.grpc.gateway.operations.client import (
    OperationsGatewayGRPCClient,
    build_operations_gateway_locust_grpc_client
)
from clients.grpc.gateway.users.client import UsersGatewayGRPCClient, build_users_gateway_locust_grpc_client


class GatewayGRPCTaskSet(TaskSet):
    """
    Базовый TaskSet для gRPC-сценариев, работающих с grpc-gateway.

    Здесь создаются все необходимые API клиенты, которые будут доступны в последующих задачах (task).
    Используется, если порядок выполнения задач внутри таск-сета не имеет значения.
    """

    # Аннотации полей с клиентами (появятся в self после on_start)
    users_gateway_client: UsersGatewayGRPCClient
    cards_gateway_client: CardsGatewayGRPCClient
    accounts_gateway_client: AccountsGatewayGRPCClient
    documents_gateway_client: DocumentsGatewayGRPCClient
    operations_gateway_client: OperationsGatewayGRPCClient

    def on_start(self) -> None:
        """
        Метод вызывается перед запуском задач TaskSet.
        Здесь создаются API клиенты с использованием контекста окружения Locust.
        """
        self.users_gateway_client = build_users_gateway_locust_grpc_client(self.user.environment)
        self.cards_gateway_client = build_cards_gateway_locust_grpc_client(self.user.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_grpc_client(self.user.environment)
        self.documents_gateway_client = build_documents_gateway_locust_grpc_client(self.user.environment)
        self.operations_gateway_client = build_operations_gateway_locust_grpc_client(self.user.environment)


class GatewayGRPCSequentialTaskSet(SequentialTaskSet):
    """
    Базовый SequentialTaskSet для gRPC-сценариев, где важен порядок выполнения задач.

    Задачи внутри такого таск-сета будут выполняться строго по очереди — сверху вниз.
    Также здесь инициализируются те же API клиенты, что и в обычном TaskSet.
    """
    users_gateway_client: UsersGatewayGRPCClient
    cards_gateway_client: CardsGatewayGRPCClient
    accounts_gateway_client: AccountsGatewayGRPCClient
    documents_gateway_client: DocumentsGatewayGRPCClient
    operations_gateway_client: OperationsGatewayGRPCClient

    def on_start(self) -> None:
        """
        Создание API клиентов для последовательного сценария.
        """
        self.users_gateway_client = build_users_gateway_locust_grpc_client(self.user.environment)
        self.cards_gateway_client = build_cards_gateway_locust_grpc_client(self.user.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_grpc_client(self.user.environment)
        self.documents_gateway_client = build_documents_gateway_locust_grpc_client(self.user.environment)
        self.operations_gateway_client = build_operations_gateway_locust_grpc_client(self.user.environment)
