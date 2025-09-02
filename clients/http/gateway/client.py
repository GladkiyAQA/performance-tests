from typing import Any

from httpx import Client, URL, Response, QueryParams


class HTTPClient:
    """
    Базовый HTTP API клиент, принимающий объект httpx.Client.

    :param client: экземпляр httpx.Client для выполнения HTTP-запросов
    """

    def __init__(self, client: Client):
        self.client = client

    def get(self, url: URL | str, params: QueryParams | None = None) -> Response:
        """
        Выполняет GET-запрос.

        :param url: URL-адрес эндпоинта.
        :param params: GET-параметры запроса (например, ?key=value).
        :return: Объект Response с данными ответа.
        """
        return self.client.get(url, params=params)

    def post(self, url: str, json: Any | None = None) -> Response:
        """
        Выполняет POST-запрос.

        :param url: URL-адрес эндпоинта.
        :param json: Данные в формате JSON.
        :return: Объект Response с данными ответа.
        """
        return self.client.post(url=url, json=json)