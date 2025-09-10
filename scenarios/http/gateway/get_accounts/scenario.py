from locust import TaskSet, task

from clients.http.gateway.users.schema import CreateUserResponseSchema
from clients.http.gateway.accounts.schema import OpenDepositAccountResponseSchema
from clients.http.gateway.gateway_task_set import GatewayHTTPTaskSet
from tools.locust.base_user import LocustBaseUser


class GetAccountsTaskSet(GatewayHTTPTaskSet, TaskSet):
    """
    Нагрузочный сценарий:
    1. Создание пользователя
    2. Открытие депозитного счёта
    3. Получение списка счетов
    Задачи выполняются в произвольном порядке.
    """

    create_user_response: CreateUserResponseSchema | None = None
    open_deposit_account_response: OpenDepositAccountResponseSchema | None = None

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


class GetDocumentsScenarioUser(LocustBaseUser):
    """
    Пользователь Locust, исполняющий последовательный сценарий получения документов.
    """
    tasks = [GetAccountsTaskSet]
