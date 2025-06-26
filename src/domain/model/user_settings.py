from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserSettings:
    chat_id: str
    min_days: int
    max_days: int
    last_sent: datetime = None
