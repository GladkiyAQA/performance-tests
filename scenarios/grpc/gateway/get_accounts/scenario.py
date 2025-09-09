from locust import User, TaskSet, task, between

from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse
from contracts.services.gateway.accounts.rpc_open_deposit_account_pb2 import OpenDepositAccountResponse
from clients.grpc.gateway.gateway_task_set import GatewayGRPCTaskSet


class GetAccountsTaskSet(GatewayGRPCTaskSet, TaskSet):
    """
    gRPC сценарий:
    1. Создание пользователя
    2. Открытие депозитного счёта
    3. Получение списка счетов
    """

    create_user_response: CreateUserResponse | None = None
    open_deposit_account_response: OpenDepositAccountResponse | None = None

    @task(2)
    def create_user(self):
        """Создание нового пользователя"""
        self.create_user_response = self.users_gateway_client.create_user()

    @task(2)
    def open_deposit_account(self):
        """Открытие депозитного счёта (если есть пользователь)"""
        if not self.create_user_response:
            return
        self.open_deposit_account_response = self.accounts_gateway_client.open_deposit_account(
            user_id=self.create_user_response.user.id
        )

    @task(6)
    def get_accounts(self):
        """Получение списка всех счетов (если есть пользователь)"""
        if not self.create_user_response:
            return
        self.accounts_gateway_client.get_accounts(
            user_id=self.create_user_response.user.id
        )


class GetAccountsScenarioUser(User):
    host = "localhost"
    wait_time = between(1, 3)
    tasks = [GetAccountsTaskSet]
