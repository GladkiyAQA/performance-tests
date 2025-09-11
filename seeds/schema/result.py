import random

from pydantic import BaseModel, Field


class SeedCardResult(BaseModel):
    """
    Результат генерации карты.

    Attributes:
        card_id (str): Уникальный идентификатор карты.
    """
    card_id: str


class SeedOperationResult(BaseModel):
    """
    Результат генерации операции.

    Attributes:
        operation_id (str): Уникальный идентификатор операции.
    """
    operation_id: str


class SeedAccountResult(BaseModel):
    """
    Результат генерации счёта с вложенными сущностями.

    Attributes:
        account_id (str): Уникальный идентификатор счёта.
        physical_cards (list[SeedCardResult]): Список физических карт, привязанных к счёту.
        top_up_operations (list[SeedOperationResult]): Список операций пополнения.
        purchase_operations (list[SeedOperationResult]): Список операций покупки.
    """
    account_id: str
    physical_cards: list[SeedCardResult] = Field(default_factory=list)
    top_up_operations: list[SeedOperationResult] = Field(default_factory=list)
    purchase_operations: list[SeedOperationResult] = Field(default_factory=list)


class SeedUserResult(BaseModel):
    """
    Результат генерации пользователя с привязанными счетами.

    Attributes:
        user_id (str): Уникальный идентификатор пользователя.
        deposit_accounts (list[SeedAccountResult]): Список депозитных счетов.
        savings_accounts (list[SeedAccountResult]): Список сберегательных счетов.
        debit_card_accounts (list[SeedAccountResult]): Список дебетовых счетов.
        credit_card_accounts (list[SeedAccountResult]): Список кредитных счетов.
    """
    user_id: str
    deposit_accounts: list[SeedAccountResult] = Field(default_factory=list)
    savings_accounts: list[SeedAccountResult] = Field(default_factory=list)
    debit_card_accounts: list[SeedAccountResult] = Field(default_factory=list)
    credit_card_accounts: list[SeedAccountResult] = Field(default_factory=list)


class SeedsResult(BaseModel):
    """
    Главная модель результата сидинга — агрегирует всех созданных пользователей.

    Attributes:
        users (list[SeedUserResult]): Список сгенерированных пользователей.
    """

    users: list[SeedUserResult] = Field(default_factory=list)

    def get_next_user(self) -> SeedUserResult:
        """
        Возвращает и удаляет первого пользователя из списка.

        Используется в случае, когда на каждый виртуальный юзер нужен новый тестовый пользователь.
        Удобно при строго последовательной раздаче пользователей в тестовых сценариях.

        Returns:
            SeedUserResult: Следующий пользователь из списка.
        """
        return self.users.pop(0)

    def get_random_user(self) -> SeedUserResult:
        """
        Возвращает случайного пользователя из списка без удаления.

        Используется в ситуациях, когда порядок не имеет значения, и пользователь выбирается случайно.

        Returns:
            SeedUserResult: Случайный пользователь.
        """
        return random.choice(self.users)
