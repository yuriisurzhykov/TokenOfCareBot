from abc import ABC, abstractmethod
from datetime import datetime

from src.domain.model.user_settings import UserSettings


class ScheduleDeterminer(ABC):
    """
    Доменный сервис: на основе last_sent и интервала определяет
    точное время следующей отправки.
    """

    @abstractmethod
    def determine_next(self, settings: UserSettings, interval_days: int) -> datetime:
        """
        Вернуть datetime, когда нужно отправить следующий подарок.
        """
        ...
