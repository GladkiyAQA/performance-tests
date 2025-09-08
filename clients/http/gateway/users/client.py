import time

from httpx import Response
from locust.env import Environment

from clients.http.client import HTTPClient, HTTPClientExtensions
from clients.http.gateway.client import build_gateway_http_client, build_gateway_locust_http_client
from clients.http.gateway.users.schema import (
    GetUserResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema
)



class UsersGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/users сервиса http-gateway.
    """

    def get_user_api(self, user_id: str) -> Response:
        """
        Получить данные пользователя по его user_id.

        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(
            f"/api/v1/users/{user_id}",
            extensions=HTTPClientExtensions(route="/api/v1/users/{user_id}")
        )

    # Теперь используем pydantic-модель для аннотации
    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """
        Создание нового пользователя.

        :param request: Pydantic-модель с данными нового пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """
        # Сериализуем модель в словарь с использованием alias
        return self.post("/api/v1/users", json=request.model_dump(by_alias=True))

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        response = self.get_user_api(user_id)
        # Инициализируем модель через валидацию JSON строки
        return GetUserResponseSchema.model_validate_json(response.text)

    # Теперь используем pydantic-модель для аннотации
    def create_user(self) -> CreateUserResponseSchema:
        request = CreateUserRequestSchema()
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)


def build_users_gateway_http_client() -> UsersGatewayHTTPClient:
    """
    Функция создаёт экземпляр UsersGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию UsersGatewayHTTPClient.
    """
    return UsersGatewayHTTPClient(client=build_gateway_http_client())

def build_users_gateway_locust_http_client(environment: Environment) -> UsersGatewayHTTPClient:
    """
    Функция создаёт экземпляр UsersGatewayHTTPClient адаптированного под Locust.

    Клиент автоматически собирает метрики и передаёт их в Locust через хуки.
    Используется исключительно в нагрузочных тестах.

    :param environment: объект окружения Locust.
    :return: экземпляр UsersGatewayHTTPClient с хуками сбора метрик.
    """
    return UsersGatewayHTTPClient(client=build_gateway_locust_http_client(environment))
