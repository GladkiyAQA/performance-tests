from abc import ABC, abstractmethod

from seeds.builder import build_grpc_seeds_builder
from seeds.dumps import save_seeds_result, load_seeds_result
from seeds.schema.plan import SeedsPlan
from seeds.schema.result import SeedsResult


class SeedsScenario(ABC):
    """
    Абстрактный класс для работы со сценариями сидинга.
    Этот класс инкапсулирует общую логику генерации, сохранения и загрузки данных для тестов.
    """

    def __init__(self):
        """
        Инициализация класса SeedsScenario.
        Создаёт экземпляр билдера для генерации сидинговых данных через gRPC.
        """
        self.builder = build_grpc_seeds_builder()

    @property
    @abstractmethod
    def plan(self) -> SeedsPlan:
        """
        Абстрактное свойство для получения плана сидинга.
        Должно быть переопределено в дочерних классах.
        """
        ...

    @property
    @abstractmethod
    def scenario(self) -> str:
        """
        Абстрактное свойство для получения имени сценария сидинга.
        Должно быть переопределено в дочерних классах.
        """
        ...

    def save(self, result: SeedsResult) -> None:
        """
        Сохраняет результат сидинга в файл.
        :param result: Объект SeedsResult, содержащий сгенерированные данные.
        """
        save_seeds_result(result=result, scenario=self.scenario)

    def load(self) -> SeedsResult:
        """
        Загружает результаты сидинга из файла.
        :return: Объект SeedsResult, содержащий данные, загруженные из файла.
        """
        return load_seeds_result(scenario=self.scenario)

    def build(self) -> None:
        """
        Генерирует данные с помощью билдера, используя план сидинга, и сохраняет результат.
        """
        result = self.builder.build(self.plan)
        self.save(result)
