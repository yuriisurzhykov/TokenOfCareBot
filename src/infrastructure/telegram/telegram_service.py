import os
from typing import Optional

from telegram import Bot


class TelegramService:
    """
    Обёртка над Telegram Bot API для отправки сообщений.
    Отвечает только за передачу текста в чат.
    """

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")
        # Bot из python-telegram-bot v20+ поддерживает async
        self.bot = Bot(token=self.token)

    async def send_message(self, chat_id: str, text: str) -> None:
        """
        Асинхронно отправляет текстовое сообщение в указанный чат.
        """
        await self.bot.send_message(chat_id=chat_id, text=text)
