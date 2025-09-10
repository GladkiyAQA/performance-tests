from locust import task

# Импортируем схемы ответов, чтобы типизировать shared state
from clients.http.gateway.accounts.schema import OpenSavingsAccountResponseSchema
from clients.http.gateway.gateway_task_set import GatewayHTTPSequentialTaskSet
from clients.http.gateway.users.schema import CreateUserResponseSchema
from tools.locust.base_user import LocustBaseUser


class GetDocumentsSequentialTaskSet(GatewayHTTPSequentialTaskSet):
    """
    Нагрузочный сценарий, который последовательно:
    1. Создаёт нового пользователя.
    2. Открывает сберегательный счёт.
    3. Получает документы по счёту (тариф и контракт).

    Использует базовый GatewayHTTPSequentialTaskSet и уже созданных в нём API клиентов.
    """

    # Shared state — сохраняем результаты запросов для дальнейшего использования
    create_user_response: CreateUserResponseSchema | None = None
    open_savings_account_response: OpenSavingsAccountResponseSchema | None = None

    @task
    def create_user(self):
        """
        Создаём нового пользователя и сохраняем результат для последующих шагов.
        """
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_savings_account(self):
        """
        Открываем сберегательный счёт для созданного пользователя.
        Проверяем, что предыдущий шаг был успешным.
        """
        if not self.create_user_response:
            return  # Если пользователь не был создан, нет смысла продолжать

        self.open_savings_account_response = self.accounts_gateway_client.open_savings_account(
            user_id=self.create_user_response.user.id
        )

    @task
    def get_documents(self):
        """
        Получаем документы, если счёт был успешно открыт.
        """
        if not self.open_savings_account_response:
            return  # Если счёт не открыт, запрос документов невозможен

        self.documents_gateway_client.get_tariff_document(
            account_id=self.open_savings_account_response.account.id
        )
        self.documents_gateway_client.get_contract_document(
            account_id=self.open_savings_account_response.account.id
        )


class GetDocumentsScenarioUser(LocustBaseUser):  # Наследуем от базового класса
    """
    Пользователь Locust, исполняющий последовательный сценарий получения документов.
    """
    tasks = [GetDocumentsSequentialTaskSet]  # Указываем только задачи
