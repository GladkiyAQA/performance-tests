import os

from seeds.schema.result import SeedsResult
from tools.logger import get_logger

logger = get_logger("SEEDS_DUMPS")


def save_seeds_result(result: SeedsResult, scenario: str):
    """
    Сохраняет результат сидинга (SeedsResult) в JSON-файл.
    """
    if not os.path.exists("dumps"):
        os.mkdir("dumps")

    seeds_file = f"./dumps/{scenario}_seeds.json"

    with open(seeds_file, 'w+', encoding="utf-8") as file:
        file.write(result.model_dump_json())

    logger.debug(f"Seeding result saved to file: {seeds_file}")


def load_seeds_result(scenario: str) -> SeedsResult:
    """
    Загружает результат сидинга из JSON-файла.
    """
    seeds_file = f'./dumps/{scenario}_seeds.json'

    with open(seeds_file, 'r', encoding="utf-8") as file:
        result = SeedsResult.model_validate_json(file.read())

    logger.debug(f"Seeding result loaded from file: {seeds_file}")

    return result
