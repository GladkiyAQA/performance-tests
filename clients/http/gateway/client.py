import logging

from httpx import Client
from locust.env import Environment


from clients.http.event_hooks.locust_event_hook import locust_request_event_hook, locust_response_event_hook


def build_gateway_http_client() -> Client:
    """
    Функция создаёт экземпляр httpx.Client с базовыми настройками для сервиса http-gateway.

    :return: Готовый к использованию объект httpx.Client.
    """
    return Client(timeout=100, base_url="http://localhost:8003")

def build_gateway_locust_http_client(environment: Environment) -> Client:
    """
    HTTP-клиент, предназначенный специально для нагрузочного тестирования с помощью Locust.

    Отличается от обычного клиента тем, что:
    - добавляет хук `locust_request_event_hook` для фиксации времени начала запроса,
    - добавляет хук `locust_response_event_hook`, который вычисляет метрики
    (время ответа, длину ответа и т.д.) и отправляет их в Locust через `environment.events.request`.

    Таким образом, данный клиент автоматически репортит статистику в Locust
    при каждом выполненном HTTP-запросе.

    :param environment: Объект окружения Locust, необходим для генерации событий метрик.
    :return: httpx.Client с подключёнными хуками под нагрузочное тестирование.
    """
    # Подавляем INFO-логи httpx (например: "HTTP Request: GET ... 200 OK")
    # Это избавляет консоль от лишнего вывода при высоконагруженных тестах
    logging.getLogger("httpx").setLevel(logging.WARNING)

    return Client(
        timeout=100,
        base_url="http://localhost:8003",
        event_hooks={
            "request": [locust_request_event_hook],  # Отмечаем время начала запроса
            "response": [locust_response_event_hook(environment)]  # Собираем метрики и передаём их в Locust
        }
    )