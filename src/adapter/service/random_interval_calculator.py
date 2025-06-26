import random

from src.domain.model.user_settings import UserSettings
from src.domain.service.interval_calculator import IntervalCalculator


class RandomIntervalCalculator(IntervalCalculator):
    def calculate(self, settings: UserSettings) -> int:
        return random.randint(settings.min_days, settings.max_days)
