import time

from grpc import RpcError, UnaryUnaryClientInterceptor
from locust.env import Environment


class LocustInterceptor(UnaryUnaryClientInterceptor):
    """
    gRPC-интерцептор для сбора метрик Locust.
    Используется для измерения времени выполнения вызовов и регистрации успехов/ошибок.
    """

    def __init__(self, environment: Environment):
        """
        :param environment: Экземпляр среды Locust, содержащий события сбора метрик.
        """
        self.environment = environment

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """
        Метод-перехватчик для unary-unary gRPC вызовов.

        :param continuation: Функция, вызывающая фактический gRPC метод.
        :param client_call_details: Детали запроса (метод, метаданные, таймаут и т.д.).
        :param request: Объект запроса, отправляемый на сервер.
        :return: gRPC response (future объект).
        """
        response = None
        exception: RpcError | None = None
        start_time = time.perf_counter()  # Засекаем время начала запроса
        response_length = 0

        try:
            # Выполняем gRPC вызов и получаем response future
            response = continuation(client_call_details, request)

            # Получаем размер ответа, если он уже доступен (для метрик)
            response_length = response.result().ByteSize()
        except RpcError as error:
            # В случае ошибки сохраняем исключение для метрик
            exception = error

        # Регистрируем вызов в системе метрик Locust
        self.environment.events.request.fire(
            name=client_call_details.method,  # Имя метода (например, "/users.UsersService/CreateUser")
            context=None,  # Можно использовать для передачи кастомных данных
            response=response,  # Объект ответа (если нужен для контекста)
            exception=exception,  # Если произошла ошибка — передаём её сюда
            request_type="gRPC",  # Тип запроса (например, "HTTP", "gRPC")
            response_time=(time.perf_counter() - start_time) * 1000,  # Время выполнения в миллисекундах
            response_length=response_length,  # Размер ответа в байтах
        )

        # Возвращаем результат вызова (future-объект)
        return response
