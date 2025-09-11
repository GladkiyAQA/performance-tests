from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedAccountsPlan


class ExistingUserGetDocumentsSeedsScenario(SeedsScenario):
    """
    Сценарий сидинга для существующего пользователя, который просматривает свои счета и документы.
    Создаём 100 пользователей, каждому из которых открываются дебетовый и сберегательный счёт.
    """

    @property
    def plan(self) -> SeedsPlan:
        """
        Возвращает план сидинга для создания пользователей и их счетов.
        Мы создаём 100 пользователей, каждый получит дебетовый и сберегательный счёт.
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=100,  # Создаём 100 пользователей
                savings_accounts=SeedAccountsPlan(count=1),  # Сберегательный счёт на пользователя
                debit_card_accounts=SeedAccountsPlan(count=1)  # Дебетовый счёт на пользователя
            ),
        )

    @property
    def scenario(self) -> str:
        """
        Возвращает название сценария сидинга.
        Это имя будет использоваться для сохранения данных сидинга.
        """
        return "existing_user_get_documents"


if __name__ == '__main__':
    """
    Запуск сценария сидинга вручную.
    Создаём объект сценария и вызываем метод build для создания данных.
    """
    seeds_scenario = ExistingUserGetDocumentsSeedsScenario()
    seeds_scenario.build()  # Запуск сидинга
