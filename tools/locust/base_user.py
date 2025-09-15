from locust import User, between

from config import settings


class LocustBaseUser(User):
    """
    Базовый виртуальный пользователь Locust, от которого наследуются все сценарии.
    Содержит общие настройки, которые могут быть переопределены при необходимости.
    """
    host: str = "localhost"
    abstract = True
    wait_time = between(
        min_wait=settings.locust_user.wait_time_min,
        max_wait=settings.locust_user.wait_time_max
    )
