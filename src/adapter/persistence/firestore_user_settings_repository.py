from typing import Optional

from src.domain.model.user_settings import UserSettings
from src.domain.repository.user_settings_repository import UserSettingsRepository
from src.infrastructure.persistence.firestore_service import FirestoreService


class FirestoreUserSettingsRepository(UserSettingsRepository):
    """Адаптер, реализующий UserSettingsRepository через FirestoreService."""
    COLLECTION = "user_settings"

    def __init__(self, fs: FirestoreService):
        self.fs = fs

    def get_by_chat_id(self, chat_id: str) -> Optional[UserSettings]:
        data = self.fs.get_document(self.COLLECTION, chat_id)
        if not data:
            return None
        return UserSettings(
            chat_id=chat_id,
            min_days=data["min_days"],
            max_days=data["max_days"],
            last_sent=data.get("last_sent")
        )

    def save(self, settings: UserSettings) -> None:
        payload = {
            "min_days": settings.min_days,
            "max_days": settings.max_days,
            "last_sent": settings.last_sent.isoformat() if settings.last_sent else None
        }
        self.fs.set_document(self.COLLECTION, settings.chat_id, payload)

    def list_all(self) -> list:
        docs = self.fs.list_documents(self.COLLECTION)
        return [
            UserSettings(
                chat_id=d.get("chat_id"),
                min_days=d.get("min_days"),
                max_days=d.get("max_days"),
                last_sent=d.get("last_sent")
            ) for d in docs
        ]
