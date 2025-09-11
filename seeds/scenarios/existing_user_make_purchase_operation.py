from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedCardsPlan, SeedAccountsPlan


class ExistingUserMakePurchaseOperationSeedsScenario(SeedsScenario):
    """
    Сценарий сидинга для существующего пользователя, который выполняет операцию покупки.
    Создаёт 300 пользователей, открывает кредитный счёт и выдаёт карты.
    """

    @property
    def plan(self) -> SeedsPlan:
        """
        План сидинга, который описывает, сколько пользователей нужно создать
        и какие именно данные для них генерировать.
        В данном случае создаём 300 пользователей, каждому даём кредитный счёт и карту.
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,  # Количество пользователей
                credit_card_accounts=SeedAccountsPlan(
                    count=1,  # Количество счётов на пользователя
                    physical_cards=SeedCardsPlan(count=1)  # Количество физических карт
                )
            ),
        )

    @property
    def scenario(self) -> str:
        """
        Название сценария сидинга, которое будет использоваться для сохранения данных.
        """
        return "existing_user_make_purchase_operation"


if __name__ == '__main__':
    # Если файл запускается напрямую, создаём объект сценария и запускаем его.
    seeds_scenario = ExistingUserMakePurchaseOperationSeedsScenario()
    seeds_scenario.build()  # Стартуем процесс сидинга
