from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.model.user_settings import UserSettings


class UserSettingsRepository(ABC):
    """
    Интерфейс репозитория для хранения и получения настроек пользователей.
    Каждый конкретный адаптер (Firestore, SQLite, in-memory и т.п.) реализует этот интерфейс.
    """

    @abstractmethod
    def get_by_chat_id(self, chat_id: str) -> Optional[UserSettings]:
        """
        Возвращает UserSettings для данного chat_id,
        или None, если запись не найдена.
        """

    @abstractmethod
    def save(self, settings: UserSettings) -> None:
        """
        Сохраняет или обновляет (upsert) настройки пользователя.
        """

    @abstractmethod
    def list_all(self) -> List[UserSettings]:
        """
        Возвращает список всех UserSettings,
        например, для перепланирования задач при старте.
        """
