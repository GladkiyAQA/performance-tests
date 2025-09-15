import logging


def get_logger(name: str) -> logging.Logger:
    # Инициализация логгера с указанным именем
    logger = logging.getLogger(name)
    # Устанавливаем уровень логирования DEBUG для логгера,
    # чтобы он обрабатывал все сообщения от DEBUG и выше
    logger.setLevel(logging.DEBUG)

    # Проверяем, есть ли уже добавленные обработчики у логгера.
    # Это необходимо, чтобы избежать дублирования логов, особенно в тех случаях,
    # когда логгер уже был сконфигурирован внешней системой, например Locust или pytest.
    # Без этой проверки обработчик StreamHandler будет добавляться каждый раз заново,
    # из-за чего каждое лог-сообщение будет выводиться по два и более раза.
    if not logger.hasHandlers():
        # Создаем обработчик, который будет выводить логи в консоль
        handler = logging.StreamHandler()
        # Устанавливаем уровень логирования DEBUG для обработчика,
        # чтобы он обрабатывал все сообщения от DEBUG и выше
        handler.setLevel(logging.DEBUG)

        # Задаем форматирование лог-сообщений: включаем время, имя логгера, уровень и сообщение
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)  # Применяем форматтер к обработчику

        # Добавляем обработчик к логгеру
        logger.addHandler(handler)

    # Возвращаем настроенный логгер
    return logger
