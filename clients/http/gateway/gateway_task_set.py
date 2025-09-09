from locust import TaskSet, SequentialTaskSet

# Импортируем типы и билдеры для построения HTTP API клиентов
from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient, build_accounts_gateway_locust_http_client
from clients.http.gateway.cards.client import CardsGatewayHTTPClient, build_cards_gateway_locust_http_client
from clients.http.gateway.documents.client import (
    DocumentsGatewayHTTPClient,
    build_documents_gateway_locust_http_client
)
from clients.http.gateway.operations.client import (
    OperationsGatewayHTTPClient,
    build_operations_gateway_locust_http_client
)
from clients.http.gateway.users.client import UsersGatewayHTTPClient, build_users_gateway_locust_http_client


class GatewayHTTPTaskSet(TaskSet):
    """
    Базовый TaskSet для HTTP-сценариев, работающих с http-gateway.

    Здесь создаются все необходимые API клиенты, которые будут доступны в последующих задачах (task).
    Используется, если порядок выполнения задач внутри таск-сета не имеет значения.
    """

    # Аннотации полей с клиентами (появятся в self после on_start)
    users_gateway_client: UsersGatewayHTTPClient
    cards_gateway_client: CardsGatewayHTTPClient
    accounts_gateway_client: AccountsGatewayHTTPClient
    documents_gateway_client: DocumentsGatewayHTTPClient
    operations_gateway_client: OperationsGatewayHTTPClient

    def on_start(self) -> None:
        """
        Метод вызывается перед запуском задач TaskSet.
        Здесь создаются API клиенты с использованием контекста окружения Locust.
        """
        self.users_gateway_client = build_users_gateway_locust_http_client(self.user.environment)
        self.cards_gateway_client = build_cards_gateway_locust_http_client(self.user.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.user.environment)
        self.documents_gateway_client = build_documents_gateway_locust_http_client(self.user.environment)
        self.operations_gateway_client = build_operations_gateway_locust_http_client(self.user.environment)


class GatewayHTTPSequentialTaskSet(SequentialTaskSet):
    """
    Базовый SequentialTaskSet для HTTP-сценариев, где важен порядок выполнения задач.

    Задачи внутри такого таск-сета будут выполняться строго по очереди — сверху вниз.
    Также здесь инициализируются те же API клиенты, что и в обычном TaskSet.
    """

    users_gateway_client: UsersGatewayHTTPClient
    cards_gateway_client: CardsGatewayHTTPClient
    accounts_gateway_client: AccountsGatewayHTTPClient
    documents_gateway_client: DocumentsGatewayHTTPClient
    operations_gateway_client: OperationsGatewayHTTPClient

    def on_start(self) -> None:
        """
        Создание API клиентов для последовательного сценария.
        """
        self.users_gateway_client = build_users_gateway_locust_http_client(self.user.environment)
        self.cards_gateway_client = build_cards_gateway_locust_http_client(self.user.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.user.environment)
        self.documents_gateway_client = build_documents_gateway_locust_http_client(self.user.environment)
        self.operations_gateway_client = build_operations_gateway_locust_http_client(self.user.environment)
