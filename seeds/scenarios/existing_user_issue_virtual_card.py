from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedAccountsPlan, SeedCardsPlan


class ExistingUserIssueVirtualCardSeedsScenario(SeedsScenario):
    """
    Сценарий сидинга для существующего пользователя, который выпускает виртуальную карту.
    Создаём 300 пользователей, каждому из которых открывается один дебетовый счёт.
    """

    @property
    def plan(self) -> SeedsPlan:
        """
        План сидинга: создаём 300 пользователей, каждому — по одному дебетовому счёту.
        Для каждого счёта сразу указываем выпуск 1 виртуальной карты.
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,  # Количество пользователей
                debit_card_accounts=SeedAccountsPlan(
                    count=1,  # Один дебетовый счёт на пользователя
                    virtual_cards=SeedCardsPlan(count=1)  # Выпуск одной виртуальной карты
                )
            ),
        )

    @property
    def scenario(self) -> str:
        """
        Название сценария сидинга, используется для имени файла с результатом.
        """
        return "existing_user_issue_virtual_card"


if __name__ == '__main__':
    # Если запускать напрямую, выполняем сидинг
    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()
    seeds_scenario.build()
