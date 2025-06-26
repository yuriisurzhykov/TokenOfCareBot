from src.domain.repository.user_settings_repository import UserSettingsRepository
from src.domain.service.interval_calculator import IntervalCalculator
from src.domain.service.schedule_determiner import ScheduleDeterminer


class StartupScheduler:
    """
    Use case: при старте приложения планирует задачи для всех пользователей.
    """

    def __init__(
            self,
            repository: UserSettingsRepository,
            interval_calculator: IntervalCalculator,
            schedule_determiner: ScheduleDeterminer,
            schedule_at: callable
    ):
        self.repository = repository
        self.interval_calculator = interval_calculator
        self.schedule_determiner = schedule_determiner
        self.schedule_at = schedule_at

    def execute(self) -> None:
        for settings in self.repository.list_all():
            days = self.interval_calculator.calculate(settings)
            next_time = self.schedule_determiner.determine_next(settings, days)
            job_id = f"gift_job_{settings.chat_id}"
            self.schedule_at(job_id, next_time, self.send_placeholder, settings.chat_id)

    @staticmethod
    def send_placeholder(chat_id: str):
        # В приложение будет внедрён SendGift.execute
        pass
