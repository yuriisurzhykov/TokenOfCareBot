from src.domain.service.gift_generator import GiftGenerator
from src.infrastructure.telegram.telegram_service import TelegramService


class GenerateNow:
    """
    Use case: мгновенная генерация и отправка идеи подарка по команде.
    Не влияет на расписание следующих уведомлений.
    """

    def __init__(self, gift_generator: GiftGenerator, telegram_service: TelegramService):
        self.gift_generator = gift_generator
        self.telegram_service = telegram_service

    async def execute(self, chat_id: str) -> None:
        idea = self.gift_generator.generate()
        await self.telegram_service.send_message(chat_id, idea.text)
