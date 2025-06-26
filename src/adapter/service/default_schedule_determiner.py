from datetime import datetime, timedelta

from src.domain.model.user_settings import UserSettings
from src.domain.service.schedule_determiner import ScheduleDeterminer


class DefaultScheduleDeterminer(ScheduleDeterminer):
    def determine_next(self, settings: UserSettings, interval_days: int) -> datetime:
        last = settings.last_sent or datetime.utcnow()
        return last + timedelta(days=interval_days)
