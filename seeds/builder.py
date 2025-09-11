from clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client, AccountsGatewayGRPCClient
from clients.grpc.gateway.cards.client import build_cards_gateway_grpc_client, CardsGatewayGRPCClient
from clients.grpc.gateway.operations.client import build_operations_gateway_grpc_client, OperationsGatewayGRPCClient
from clients.grpc.gateway.users.client import build_users_gateway_grpc_client, UsersGatewayGRPCClient
from clients.http.gateway.accounts.client import build_accounts_gateway_http_client, AccountsGatewayHTTPClient
from clients.http.gateway.cards.client import build_cards_gateway_http_client, CardsGatewayHTTPClient
from clients.http.gateway.operations.client import build_operations_gateway_http_client, OperationsGatewayHTTPClient
from clients.http.gateway.users.client import build_users_gateway_http_client, UsersGatewayHTTPClient
from seeds.schema.plan import (
    SeedsPlan,
    SeedUsersPlan,
    SeedAccountsPlan,
)
from seeds.schema.result import (
    SeedsResult,
    SeedUserResult,
    SeedCardResult,
    SeedAccountResult,
    SeedOperationResult
)


class SeedsBuilder:
    """
    SeedsBuilder — генератор (сидер), формирующий необходимые тестовые или демонстрационные данные
    на основании входного плана. Работает одинаково как с HTTP, так и с gRPC клиентами.

    Attributes:
        users_gateway_client: Клиент для работы с пользователями (HTTP или gRPC)
        cards_gateway_client: Клиент для выпуска карт
        accounts_gateway_client: Клиент для открытия счетов
        operations_gateway_client: Клиент для операций (топ-ап, покупки и т.д.)
    """

    def __init__(
            self,
            users_gateway_client: UsersGatewayGRPCClient | UsersGatewayHTTPClient,
            cards_gateway_client: CardsGatewayGRPCClient | CardsGatewayHTTPClient,
            accounts_gateway_client: AccountsGatewayGRPCClient | AccountsGatewayHTTPClient,
            operations_gateway_client: OperationsGatewayGRPCClient | OperationsGatewayHTTPClient
    ):
        self.users_gateway_client = users_gateway_client
        self.cards_gateway_client = cards_gateway_client
        self.accounts_gateway_client = accounts_gateway_client
        self.operations_gateway_client = operations_gateway_client

    def build_physical_card_result(self, user_id: str, account_id: str) -> SeedCardResult:
        """
        Выпускает физическую карту для заданного пользователя и счёта.

        Args:
            user_id: Идентификатор пользователя
            account_id: Идентификатор счёта

        Returns:
            SeedCardResult: Результат с ID выпущенной карты
        """
        response = self.cards_gateway_client.issue_physical_card(
            user_id=user_id,
            account_id=account_id
        )
        return SeedCardResult(card_id=response.card.id)

    def build_top_up_operation_result(self, card_id: str, account_id: str) -> SeedOperationResult:
        """
        Выполняет операцию пополнения на карту.

        Args:
            card_id: Идентификатор карты
            account_id: Идентификатор счёта

        Returns:
            SeedOperationResult: Результат с ID выполненной операции
        """
        response = self.operations_gateway_client.make_top_up_operation(
            card_id=card_id,
            account_id=account_id
        )
        return SeedOperationResult(operation_id=response.operation.id)

    def build_purchase_operation_result(self, card_id: str, account_id: str) -> SeedOperationResult:
        """
        Выполняет операцию покупки по карте.

        Args:
            card_id: Идентификатор карты
            account_id: Идентификатор счёта

        Returns:
            SeedOperationResult: Результат с ID выполненной операции
        """
        response = self.operations_gateway_client.make_purchase_operation(
            card_id=card_id,
            account_id=account_id
        )
        return SeedOperationResult(operation_id=response.operation.id)

    def build_savings_account_result(self, user_id: str) -> SeedAccountResult:
        """
        Открывает сберегательный счёт для пользователя.

        Args:
            user_id: Идентификатор пользователя

        Returns:
            SeedAccountResult: Результат с ID созданного счёта
        """
        response = self.accounts_gateway_client.open_savings_account(user_id=user_id)
        return SeedAccountResult(account_id=response.account.id)

    def build_deposit_account_result(self, user_id: str) -> SeedAccountResult:
        """
        Открывает депозитный счёт для пользователя.

        Args:
            user_id: Идентификатор пользователя

        Returns:
            SeedAccountResult: Результат с ID созданного счёта
        """
        response = self.accounts_gateway_client.open_deposit_account(user_id=user_id)
        return SeedAccountResult(account_id=response.account.id)

    def build_debit_card_account_result(self, plan: SeedAccountsPlan, user_id: str) -> SeedAccountResult:
        """
        Открывает дебетовый счёт для пользователя и при необходимости:
        - выпускает физические карты
        - выполняет операции пополнения (top-up)
        - выполняет операции покупки

        Args:
            plan: План создания дебетового счёта (кол-во карт, операций и т.п.)
            user_id: Идентификатор пользователя

        Returns:
            SeedAccountResult: Результат с ID счёта и дополнительными действиями (карты, операции)
        """
        response = self.accounts_gateway_client.open_debit_card_account(user_id=user_id)
        card_id = response.account.cards[0].id
        account_id = response.account.id

        return SeedAccountResult(
            account_id=response.account.id,
            physical_cards=[
                self.build_physical_card_result(user_id=user_id, account_id=response.account.id)
                for _ in range(plan.physical_cards.count)
            ],
            top_up_operations=[
                self.build_top_up_operation_result(card_id=card_id, account_id=account_id)
                for _ in range(plan.top_up_operations.count)
            ],
            purchase_operations=[
                self.build_purchase_operation_result(card_id=card_id, account_id=account_id)
                for _ in range(plan.purchase_operations.count)
            ]
        )

    def build_credit_card_account_result(self, plan: SeedAccountsPlan, user_id: str) -> SeedAccountResult:
        """
        Открывает кредитный счёт и выполняет действия согласно плану:
        - выпускает физические карты
        - выполняет операции пополнения (top-up)
        - выполняет операции покупки

        Args:
            plan: План создания кредитного счёта
            user_id: Идентификатор пользователя

        Returns:
            SeedAccountResult: Результат с ID счёта и деталями операций
        """
        response = self.accounts_gateway_client.open_credit_card_account(user_id=user_id)
        card_id = response.account.cards[0].id
        account_id = response.account.id

        return SeedAccountResult(
            account_id=response.account.id,
            physical_cards=[
                self.build_physical_card_result(user_id=user_id, account_id=account_id)
                for _ in range(plan.physical_cards.count)
            ],
            top_up_operations=[
                self.build_top_up_operation_result(card_id=card_id, account_id=account_id)
                for _ in range(plan.top_up_operations.count)
            ],
            purchase_operations=[
                self.build_purchase_operation_result(card_id=card_id, account_id=account_id)
                for _ in range(plan.purchase_operations.count)
            ]
        )

    def build_user(self, plan: SeedUsersPlan) -> SeedUserResult:
        """
        Создаёт пользователя и согласно переданному плану:
        - открывает сберегательные и депозитные счета
        - создаёт дебетовые и кредитные счета с картами и операциями

        Args:
            plan: План генерации пользователя

        Returns:
            SeedUserResult: Результат с ID пользователя и всеми созданными сущностями
        """
        response = self.users_gateway_client.create_user()

        return SeedUserResult(
            user_id=response.user.id,
            savings_accounts=[
                self.build_savings_account_result(user_id=response.user.id)
                for _ in range(plan.savings_accounts.count)
            ],
            deposit_accounts=[
                self.build_deposit_account_result(user_id=response.user.id)
                for _ in range(plan.deposit_accounts.count)
            ],
            debit_card_accounts=[
                self.build_debit_card_account_result(plan=plan.debit_card_accounts, user_id=response.user.id)
                for _ in range(plan.debit_card_accounts.count)
            ],
            credit_card_accounts=[
                self.build_credit_card_account_result(plan=plan.credit_card_accounts, user_id=response.user.id)
                for _ in range(plan.credit_card_accounts.count)
            ]
        )

    def build(self, plan: SeedsPlan) -> SeedsResult:
        """
        Генерирует полную структуру данных на основе плана:
        - создаёт указанное количество пользователей
        - каждому пользователю присваиваются счета, карты и операции

        Args:
            plan: Полный план генерации данных

        Returns:
            SeedsResult: Результат с данными всех созданных пользователей
        """
        return SeedsResult(users=[self.build_user(plan=plan.users) for _ in range(plan.users.count)])


def build_grpc_seeds_builder() -> SeedsBuilder:
    """
    Фабрика для создания сидера с использованием gRPC-клиентов.

    Returns:
        SeedsBuilder: Инициализированный сидер с gRPC-клиентами
    """
    return SeedsBuilder(
        users_gateway_client=build_users_gateway_grpc_client(),
        cards_gateway_client=build_cards_gateway_grpc_client(),
        accounts_gateway_client=build_accounts_gateway_grpc_client(),
        operations_gateway_client=build_operations_gateway_grpc_client()
    )


def build_http_seeds_builder():
    """
    Фабрика для создания сидера с использованием HTTP-клиентов.

    Returns:
        SeedsBuilder: Инициализированный сидер с HTTP-клиентами
    """
    return SeedsBuilder(
        users_gateway_client=build_users_gateway_http_client(),
        cards_gateway_client=build_cards_gateway_http_client(),
        accounts_gateway_client=build_accounts_gateway_http_client(),
        operations_gateway_client=build_operations_gateway_http_client()
    )
