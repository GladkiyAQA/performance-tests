from locust import task, events
from locust.env import Environment

from clients.grpc.gateway.gateway_task_set import GatewayGRPCTaskSet
from seeds.scenarios.existing_user_issue_virtual_card import ExistingUserIssueVirtualCardSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.locust.base_user import LocustBaseUser


# Хук инициализации: сидинг перед запуском нагрузки
@events.init.add_listener
def init(environment: Environment, **kwargs):
    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()
    seeds_scenario.build()  # создаём пользователей и счета
    environment.seeds = seeds_scenario.load()  # загружаем данные из dumps


class IssueVirtualCardTaskSet(GatewayGRPCTaskSet):
    """
    Сценарий: существующий пользователь
    1. Получает список счетов
    2. Выпускает новую виртуальную карту
    """
    seed_user: SeedUserResult

    def on_start(self) -> None:
        super().on_start()
        # Берём случайного пользователя из сидинга
        self.seed_user = self.user.environment.seeds.get_random_user()

    @task(3)
    def get_accounts(self):
        # Загружаем список счетов пользователя
        self.accounts_gateway_client.get_accounts(user_id=self.seed_user.user_id)

    @task(1)
    def issue_virtual_card(self):
        # Выпускаем виртуальную карту для дебетового счёта
        self.cards_gateway_client.issue_virtual_card(
            user_id=self.seed_user.user_id,
            account_id=self.seed_user.debit_card_accounts[0].account_id
        )


class IssueVirtualCardScenarioUser(LocustBaseUser):
    """
    Виртуальный пользователь Locust, исполняющий сценарий выпуска виртуальной карты.
    """
    tasks = [IssueVirtualCardTaskSet]
