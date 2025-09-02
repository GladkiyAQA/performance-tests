from httpx import Response, QueryParams

from clients.http.client import HTTPClient
from clients.http.gateway.accounts.schema import (
    GetAccountsQuerySchema,
    GetAccountsResponseSchema,
    OpenDepositAccountRequestSchema,
    OpenDepositAccountResponseSchema,
    OpenSavingsAccountRequestSchema,
    OpenSavingsAccountResponseSchema,
    OpenDebitCardAccountRequestSchema,
    OpenDebitCardAccountResponseSchema,
    OpenCreditCardAccountRequestSchema,
    OpenCreditCardAccountResponseSchema
)
from clients.http.gateway.client import build_gateway_http_client


class AccountsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/accounts сервиса http-gateway.
    """

    def get_accounts_api(self, query: GetAccountsQuerySchema):
        """
        Выполняет GET-запрос на получение списка счетов пользователя.

        :param query: Pydantic-модель с параметрами запроса, например: {'userId': '123'}.
        :return: Объект httpx.Response с данными о счетах.
        """
        return self.get(
            "/api/v1/accounts",
            params=QueryParams(**query.model_dump(by_alias=True))
        )

    def open_deposit_account_api(self, request: OpenDepositAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия депозитного счёта.

        :param request: Pydantic-модель с userId.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(
            "/api/v1/accounts/open-deposit-account",
            json=request.model_dump(by_alias=True)
        )

    def open_savings_account_api(self, request: OpenSavingsAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия сберегательного счёта.

        :param request: Pydantic-модель с userId.
        :return: Объект httpx.Response.
        """
        return self.post(
            "/api/v1/accounts/open-savings-account",
            json=request.model_dump(by_alias=True)
        )

    def open_debit_card_account_api(self, request: OpenDebitCardAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия дебетовой карты.

        :param request: Pydantic-модель с userId.
        :return: Объект httpx.Response.
        """
        return self.post(
            "/api/v1/accounts/open-debit-card-account",
            json=request.model_dump(by_alias=True)
        )

    def open_credit_card_account_api(self, request: OpenCreditCardAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия кредитной карты.

        :param request: Pydantic-модель с userId.
        :return: Объект httpx.Response.
        """
        return self.post(
            "/api/v1/accounts/open-credit-card-account",
            json=request.model_dump(by_alias=True)
        )

    def get_accounts(self, user_id: str) -> GetAccountsResponseSchema:
        query = GetAccountsQuerySchema(user_id=user_id)
        response = self.get_accounts_api(query)
        return GetAccountsResponseSchema.model_validate_json(response.text)

    def open_deposit_account(self, user_id: str) -> OpenDepositAccountResponseSchema:
        request = OpenDepositAccountRequestSchema(user_id=user_id)
        response = self.open_deposit_account_api(request)
        return OpenDepositAccountResponseSchema.model_validate_json(response.text)

    def open_savings_account(self, user_id: str) -> OpenSavingsAccountResponseSchema:
        request = OpenSavingsAccountRequestSchema(user_id=user_id)
        response = self.open_savings_account_api(request)
        return OpenSavingsAccountResponseSchema.model_validate_json(response.text)

    def open_debit_card_account(self, user_id: str) -> OpenDebitCardAccountResponseSchema:
        request = OpenDebitCardAccountRequestSchema(user_id=user_id)
        response = self.open_debit_card_account_api(request)
        return OpenDebitCardAccountResponseSchema.model_validate_json(response.text)

    def open_credit_card_account(self, user_id: str) -> OpenCreditCardAccountResponseSchema:
        request = OpenCreditCardAccountRequestSchema(user_id=user_id)
        response = self.open_credit_card_account_api(request)
        return OpenCreditCardAccountResponseSchema.model_validate_json(response.text)


def build_accounts_gateway_http_client() -> AccountsGatewayHTTPClient:
    """
    Функция создаёт экземпляр AccountsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AccountsGatewayHTTPClient.
    """
    return AccountsGatewayHTTPClient(client=build_gateway_http_client())
