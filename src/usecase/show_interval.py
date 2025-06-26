from src.domain.repository.user_settings_repository import UserSettingsRepository


class ShowInterval:
    """
    Use case для команды /showinterval: возвращает строку с текущим интервалом.
    """

    def __init__(self, repository: UserSettingsRepository):
        self.repository = repository

    def execute(self, chat_id: str) -> str:
        settings = self.repository.get_by_chat_id(chat_id)
        if not settings:
            return "Сначала запустите /start"
        return f"Текущий интервал: {settings.min_days}–{settings.max_days} дней."
