from abc import ABC, abstractmethod

from src.domain.model.user_settings import UserSettings


class IntervalCalculator(ABC):
    """
    Доменный сервис: на основе настроек пользователя рассчитывает
    случайное количество дней до следующей отправки.
    """

    @abstractmethod
    def calculate(self, settings: UserSettings) -> int:
        """
        Вернуть случайное число дней в диапазоне [min_days, max_days].
        """
        ...
