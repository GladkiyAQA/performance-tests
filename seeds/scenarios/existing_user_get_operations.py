from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedAccountsPlan, SeedOperationsPlan


class ExistingUserGetOperationsSeedsScenario(SeedsScenario):
    """
    Сценарий сидинга для существующего пользователя, который просматривает список операций по счёту.
    Создаём 300 пользователей, каждому открывается кредитный счёт, на который генерируются операции:
    - 5 покупок
    - 1 пополнение
    - 1 снятие наличных
    """

    @property
    def plan(self) -> SeedsPlan:
        """
        План сидинга: создаём 300 пользователей, каждому выдаём один кредитный счёт.
        Для каждого счёта генерируем 5 покупок, 1 пополнение и 1 снятие наличных.
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,  # Количество пользователей
                credit_card_accounts=SeedAccountsPlan(
                    count=1,  # Один кредитный счёт на пользователя
                    purchase_operations=SeedOperationsPlan(count=5),  # 5 операций покупки
                    top_up_operations=SeedOperationsPlan(count=1),  # 1 операция пополнения
                    cash_withdrawal_operations=SeedOperationsPlan(count=1),  # 1 операция снятия наличных
                )
            ),
        )

    @property
    def scenario(self) -> str:
        """
        Название сценария сидинга, используется для сохранения результатов.
        """
        return "existing_user_get_operations"


if __name__ == '__main__':
    # Запуск сидинга вручную
    seeds_scenario = ExistingUserGetOperationsSeedsScenario()
    seeds_scenario.build()
