from typing import TypedDict
from httpx import Response

from clients.http.client import HTTPClient


class IssueVirtualCardRequestDict(TypedDict):
    """
    Структура данных для выпуска виртуальной карты.
    """
    userId: str
    accountId: str


class IssuePhysicalCardRequestDict(TypedDict):
    """
    Структура данных для выпуска физической карты.
    """
    userId: str
    accountId: str


class CardsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/cards сервиса http-gateway.
    """

    def issue_virtual_card_api(self, request: IssueVirtualCardRequestDict) -> Response:
        """
        Выпустить виртуальную карту для пользователя.

        :param request: Словарь с данными для выпуска виртуальной карты.
            Обязательные поля:
              - userId: str — идентификатор пользователя.
              - accountId: str — идентификатор счёта, к которому будет привязана карта.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/cards/issue-virtual-card", json=request)

    def issue_physical_card_api(self, request: IssuePhysicalCardRequestDict) -> Response:
        """
        Выпустить физическую карту для пользователя.

        :param request: Словарь с данными для выпуска физической карты.
            Обязательные поля:
              - userId: str — идентификатор пользователя.
              - accountId: str — идентификатор счёта, к которому будет привязана карта.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/cards/issue-physical-card", json=request)
