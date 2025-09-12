from locust import task

from clients.http.gateway.accounts.schema import OpenDebitCardAccountResponseSchema
from clients.http.gateway.gateway_task_set import GatewayHTTPSequentialTaskSet
from clients.http.gateway.operations.schema import MakeTopUpOperationResponseSchema
from clients.http.gateway.users.schema import CreateUserResponseSchema
from tools.locust.base_user import LocustBaseUser


# Класс сценария: описывает последовательный флоу нового пользователя
class MakeTopUpOperationSequentialTaskSet(GatewayHTTPSequentialTaskSet):
    # Храним ответы от предыдущих шагов, чтобы использовать их в следующих задачах
    create_user_response: CreateUserResponseSchema | None = None
    make_top_up_operation_response: MakeTopUpOperationResponseSchema | None = None
    open_open_debit_card_account_response: OpenDebitCardAccountResponseSchema | None = None

    @task
    def create_user(self):
        # Первый шаг — создать нового пользователя
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self):
        # Невозможно открыть счёт без созданного пользователя
        if not self.create_user_response:
            return

        # Открываем дебетовый счёт для нового пользователя
        self.open_open_debit_card_account_response = self.accounts_gateway_client.open_debit_card_account(
            user_id=self.create_user_response.user.id
        )

    @task
    def make_top_up_operation(self):
        # Проверяем, что счёт успешно открыт
        if not self.open_open_debit_card_account_response:
            return

        # Выполняем операцию пополнения счёта
        self.make_top_up_operation_response = self.operations_gateway_client.make_top_up_operation(
            card_id=self.open_open_debit_card_account_response.account.cards[0].id,
            account_id=self.open_open_debit_card_account_response.account.id
        )

    @task
    def get_operations(self):
        # Получаем список операций по счёту
        if not self.open_open_debit_card_account_response:
            return

        self.operations_gateway_client.get_operations(
            account_id=self.open_open_debit_card_account_response.account.id
        )

    @task
    def get_operations_summary(self):
        # Получаем агрегированную статистику по операциям
        if not self.open_open_debit_card_account_response:
            return

        self.operations_gateway_client.get_operations_summary(
            account_id=self.open_open_debit_card_account_response.account.id
        )

    @task
    def get_operation(self):
        # Получаем детальную информацию по операции пополнения
        if not self.make_top_up_operation_response:
            return

        self.operations_gateway_client.get_operation(
            operation_id=self.make_top_up_operation_response.operation.id
        )


# Класс пользователя — связывает TaskSet со средой исполнения Locust
class MakeTopUpOperationScenarioUser(LocustBaseUser):
    # Назначаем сценарий, который будет выполняться этим пользователем
    tasks = [MakeTopUpOperationSequentialTaskSet]
