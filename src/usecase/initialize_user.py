from src.domain.model.user_settings import UserSettings
from src.domain.repository.user_settings_repository import UserSettingsRepository
from src.domain.service.interval_calculator import IntervalCalculator
from src.domain.service.schedule_determiner import ScheduleDeterminer


class InitializeUser:
    """
    Use case для команды /start: создаёт настройку пользователя
    и планирует первое уведомление.
    """

    def __init__(
            self,
            repository: UserSettingsRepository,
            interval_calculator: IntervalCalculator,
            schedule_determiner: ScheduleDeterminer,
            schedule_at: callable  # функция job_queue_manager.schedule_at
    ):
        self.repository = repository
        self.interval_calculator = interval_calculator
        self.schedule_determiner = schedule_determiner
        self.schedule_at = schedule_at

    def execute(self, chat_id: str) -> str:
        # Устанавливаем дефолтный интервал 2–7 дней
        settings = UserSettings(chat_id=chat_id, min_days=2, max_days=7)
        self.repository.save(settings)

        # Рассчитываем время первого уведомления
        days = self.interval_calculator.calculate(settings)
        next_time = self.schedule_determiner.determine_next(settings, days)
        job_id = f"gift_job_{chat_id}"
        # Планируем
        self.schedule_at(job_id, next_time, self.send_placeholder, chat_id)

        return (
            "Привет! Я буду присылать идеи подарков через "
            "случайные 2–7 дней. Чтобы изменить, используй /setinterval."
        )

    @staticmethod
    def send_placeholder(chat_id: str):
        # В приложении сюда будет подставляться SendGift.execute
        pass
