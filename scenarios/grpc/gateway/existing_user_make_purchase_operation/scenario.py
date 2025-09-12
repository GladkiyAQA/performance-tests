from locust import task, events
from locust.env import Environment

from clients.grpc.gateway.gateway_task_set import GatewayGRPCTaskSet
from seeds.scenarios.existing_user_make_purchase_operation import ExistingUserMakePurchaseOperationSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.locust.base_user import LocustBaseUser


# Хук инициализации — вызывается перед началом запуска нагрузки
@events.init.add_listener
def init(environment: Environment, **kwargs):
    # Выполняем сидинг
    seeds_scenario = ExistingUserMakePurchaseOperationSeedsScenario()
    seeds_scenario.build()  # создаём пользователей, счета, карты и операции

    # Загружаем результат сидинга (из файла JSON)
    environment.seeds = seeds_scenario.load()


# TaskSet — сценарий пользователя. Каждый виртуальный пользователь выполняет эти задачи
class MakePurchaseOperationSequentialTaskSet(GatewayGRPCTaskSet):
    seed_user: SeedUserResult  # Типизированная ссылка на данные из сидинга

    def on_start(self) -> None:
        super().on_start()
        # Получаем случайного пользователя из подготовленного списка
        self.seed_user = self.user.environment.seeds.get_random_user()

    @task(1)
    def make_purchase_operation(self):
        # Совершаем покупку по первой карте пользователя
        self.operations_gateway_client.make_purchase_operation(
            card_id=self.seed_user.credit_card_accounts[0].physical_cards[0].card_id,
            account_id=self.seed_user.credit_card_accounts[0].account_id
        )

    @task(2)
    def get_accounts(self):
        # Получаем список счетов пользователя
        self.accounts_gateway_client.get_accounts(user_id=self.seed_user.user_id)

    @task(2)
    def get_operations(self):
        # Получаем список операций по счёту
        self.operations_gateway_client.get_operations(
            account_id=self.seed_user.credit_card_accounts[0].account_id
        )

    @task(2)
    def get_operations_summary(self):
        # Получаем статистику по операциям пользователя
        self.operations_gateway_client.get_operations_summary(
            account_id=self.seed_user.credit_card_accounts[0].account_id
        )


# Пользовательский класс, который будет запускать наш TaskSet
class MakePurchaseOperationScenarioUser(LocustBaseUser):
    tasks = [MakePurchaseOperationSequentialTaskSet]
