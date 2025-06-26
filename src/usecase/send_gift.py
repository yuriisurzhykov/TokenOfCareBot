from datetime import datetime

from src.domain.repository.user_settings_repository import UserSettingsRepository
from src.domain.service.gift_generator import GiftGenerator
from src.domain.service.interval_calculator import IntervalCalculator
from src.domain.service.schedule_determiner import ScheduleDeterminer
from src.infrastructure.telegram.telegram_service import TelegramService


class SendGift:
    """
    Use case: генерирует идею, отправляет в Telegram, обновляет last_sent,
    и планирует следующее уведомление.
    """

    def __init__(
            self,
            repository: UserSettingsRepository,
            gift_generator: GiftGenerator,
            telegram_service: TelegramService,
            interval_calculator: IntervalCalculator,
            schedule_determiner: ScheduleDeterminer,
            schedule_at: callable
    ):
        self.repository = repository
        self.gift_generator = gift_generator
        self.telegram_service = telegram_service
        self.interval_calculator = interval_calculator
        self.schedule_determiner = schedule_determiner
        self.schedule_at = schedule_at

    async def execute(self, chat_id: str) -> None:
        # 1. Генерация идеи
        idea = self.gift_generator.generate()
        # 2. Отправка
        await self.telegram_service.send_message(chat_id, idea.text)
        # 3. Обновление last_sent
        settings = self.repository.get_by_chat_id(chat_id)
        if settings:
            settings.last_sent = datetime.utcnow()
            self.repository.save(settings)
            # 4. Планирование следующего
            days = self.interval_calculator.calculate(settings)
            next_time = self.schedule_determiner.determine_next(settings, days)
            job_id = f"gift_job_{chat_id}"
            self.schedule_at(job_id, next_time, self.execute, chat_id)
