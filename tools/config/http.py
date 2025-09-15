from pydantic import BaseModel, HttpUrl


class HTTPClientConfig(BaseModel):
    # URL сервиса, к которому будем подключаться через httpx
    url: HttpUrl

    # Таймаут для запросов в секундах (по умолчанию 100)
    timeout: float = 100.0

    @property
    def client_url(self) -> str:
        """
        Возвращает URL в виде строки, пригодной для передачи в httpx.Client.

        Почему это важно:
        - Pydantic хранит url как объект HttpUrl.
        - httpx.Client требует base_url именно как строку.
        - Если передать HttpUrl напрямую, будет ошибка типов.
        """
        return str(self.url)


