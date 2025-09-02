from httpx import Client


def build_gateway_http_client() -> Client:
    """
    Функция создаёт экземпляр httpx.Client с базовыми настройками для сервиса http-gateway.

    :return: Готовый к использованию объект httpx.Client.
    """
    return Client(timeout=100, base_url="http://localhost:8003")
