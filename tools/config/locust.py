from pydantic import BaseModel


class LocustUserConfig(BaseModel):
    # Минимальное время ожидания между задачами (в секундах)
    wait_time_min: float = 1

    # Максимальное время ожидания между задачами (в секундах)
    wait_time_max: float = 3
