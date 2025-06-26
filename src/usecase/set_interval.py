from src.domain.model.user_settings import UserSettings
from src.domain.repository.user_settings_repository import UserSettingsRepository
from src.domain.service.interval_calculator import IntervalCalculator
from src.domain.service.schedule_determiner import ScheduleDeterminer


class SetInterval:
    """
    Use case для команды /setinterval: обновляет интервал
    и перепланирует уведомление.
    """

    def __init__(
            self,
            repository: UserSettingsRepository,
            interval_calculator: IntervalCalculator,
            schedule_determiner: ScheduleDeterminer,
            schedule_at: callable,
            remove_job: callable
    ):
        self.repository = repository
        self.interval_calculator = interval_calculator
        self.schedule_determiner = schedule_determiner
        self.schedule_at = schedule_at
        self.remove_job = remove_job

    def execute(self, chat_id: str, min_days: int, max_days: int) -> str:
        # Сохраняем новые настройки
        settings = UserSettings(chat_id=chat_id, min_days=min_days, max_days=max_days)
        self.repository.save(settings)

        job_id = f"gift_job_{chat_id}"
        # Удаляем старую задачу
        self.remove_job(job_id)

        # Планируем новую
        days = self.interval_calculator.calculate(settings)
        next_time = self.schedule_determiner.determine_next(settings, days)
        self.schedule_at(job_id, next_time, self.send_placeholder, chat_id)

        return f"Интервал изменён: случайные {min_days}–{max_days} дней."

    @staticmethod
    def send_placeholder(chat_id: str):
        # В приложение внедрят SendGift.execute
        pass
