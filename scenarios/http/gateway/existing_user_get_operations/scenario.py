from locust import task, events
from locust.env import Environment

from clients.http.gateway.gateway_task_set import GatewayHTTPTaskSet
from seeds.scenarios.existing_user_get_operations import ExistingUserGetOperationsSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.locust.base_user import LocustBaseUser


# Хук: сидинг выполняется один раз перед стартом нагрузки
@events.init.add_listener
def init(environment: Environment, **kwargs):
    seeds_scenario = ExistingUserGetOperationsSeedsScenario()
    seeds_scenario.build()  # создаём пользователей, счета и операции
    environment.seeds = seeds_scenario.load()  # загружаем из dumps


class GetOperationsTaskSet(GatewayHTTPTaskSet):
    """
    Сценарий существующего пользователя:
    - получает список счетов
    - загружает список операций
    - смотрит статистику по операциям
    """
    seed_user: SeedUserResult

    def on_start(self) -> None:
        super().on_start()
        # Выбираем случайного пользователя из сидинга
        self.seed_user = self.user.environment.seeds.get_random_user()

    @task(2)
    def get_accounts(self):
        # Получаем список счетов
        self.accounts_gateway_client.get_accounts(user_id=self.seed_user.user_id)

    @task(4)
    def get_operations(self):
        # Получаем список операций по кредитному счёту
        self.operations_gateway_client.get_operations(
            account_id=self.seed_user.credit_card_accounts[0].account_id
        )

    @task(3)
    def get_operations_summary(self):
        # Получаем агрегированную статистику
        self.operations_gateway_client.get_operations_summary(
            account_id=self.seed_user.credit_card_accounts[0].account_id
        )


class GetOperationsScenarioUser(LocustBaseUser):
    """
    Виртуальный пользователь Locust, исполняющий сценарий получения операций.
    """
    tasks = [GetOperationsTaskSet]
