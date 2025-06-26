from abc import ABC, abstractmethod

from src.domain.model.gift_idea import GiftIdea


class GiftGenerator(ABC):
    """
    Доменный сервис: генерирует одну идею подарка.
    Не знает ни про OpenAI, ни про Telegram, ни про расписание.
    """

    @abstractmethod
    def generate(self) -> GiftIdea:
        """
        Возвращает новую идею подарка.
        """
        ...
