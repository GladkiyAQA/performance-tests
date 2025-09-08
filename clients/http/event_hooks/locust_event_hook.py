import time

from httpx import Request, Response, HTTPStatusError, HTTPError
from locust.env import Environment


def locust_request_event_hook(request: Request) -> None:
    """
    HTTPX event hook, вызываемый перед отправкой запроса.

    Сохраняет текущее время в `request.extensions["start_time"]`,
    чтобы потом использовать его для расчёта времени ответа.
    """
    request.extensions["start_time"] = time.time()


def locust_response_event_hook(environment: Environment):
    """
    Возвращает HTTPX event hook, вызываемый после получения ответа.

    Использует `request.extensions["start_time"]` для вычисления времени отклика.
    Извлекает route из `request.extensions["route"]`, если задан.
    Отправляет собранные метрики в `environment.events.request`, чтобы Locust мог агрегировать статистику.

    :param environment: Объект окружения Locust, через который отправляются метрики.
    :return: Функция-хук для HTTPX response event hook.
    """

    def inner(response: Response) -> None:
        exception: HTTPError | HTTPStatusError | None = None

        try:
            # Проверка на статус ошибки (например, 500, 404 и т.д.)
            response = response.raise_for_status()
        except (HTTPError, HTTPStatusError) as error:
            exception = error

        request = response.request

        # Получаем route, если он был передан через extensions, иначе используем raw path
        route = request.extensions.get("route", request.url.path)
        # Время начала запроса, установленное в request event hook
        start_time = request.extensions.get("start_time", time.time())
        # Вычисляем длительность запроса в миллисекундах
        response_time = (time.time() - start_time) * 1000
        # Определяем размер тела ответа (можно заменить на 0, если не нужно)
        response_length = len(response.read())

        # Отправляем событие в Locust
        environment.events.request.fire(
            name=f"{request.method} {route}",  # Имя запроса (метод + логическое имя маршрута)
            context=None,  # Контекст (опционально, можно использовать для расширений)
            response=response,  # Объект ответа (опционально)
            exception=exception,  # Исключение, если оно произошло
            request_type="HTTP",  # Тип запроса (может быть любым: HTTP, gRPC, DB и т.д.)
            response_time=response_time,  # Время выполнения запроса в мс
            response_length=response_length,  # Размер тела ответа
        )

    return inner
