#!/usr/bin/env python3
"""
Telegram-бот GiftBot
"""
import dotenv

dotenv.load_dotenv()

import os
import random
from datetime import datetime, timedelta
from telegram import Update, __version__ as ptb_version
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from db import (
    get_user_settings,
    upsert_user_settings,
    list_all_user_settings
)
from gift_provider import AIProvider

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN not set")

provider = AIProvider()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = str(update.effective_chat.id)
    if not get_user_settings(chat):
        upsert_user_settings(chat, 2, 7)
    await update.message.reply_text(
        "Привет! Я пришлю идею подарка через случайный интервал 2–7 дней."
        "\n/setinterval <мин> <макс> — изменить интервал."
        "\n/showinterval — посмотреть интервал."
    )
    schedule_next(chat, context.job_queue)


async def set_interval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = str(update.effective_chat.id)
    args = context.args
    if len(args) != 2 or not all(a.isdigit() for a in args):
        return await update.message.reply_text("Используй: /setinterval <мин> <макс>")
    min_d, max_d = map(int, args)
    if min_d < 1 or max_d < min_d:
        return await update.message.reply_text("Проверь: минимум ≥1, максимум ≥минимум.")
    upsert_user_settings(chat, min_d, max_d)
    for job in context.job_queue.get_jobs_by_name(f"gift_job_{chat}"):
        job.schedule_removal()
    await update.message.reply_text(f"Интервал обновлён: {min_d}–{max_d} дней.")
    schedule_next(chat, context.job_queue)


async def show_interval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = str(update.effective_chat.id)
    cfg = get_user_settings(chat)
    if not cfg:
        return await update.message.reply_text("Сначала /start")
    await update.message.reply_text(
        f"Текущий интервал: {cfg['min_days']}–{cfg['max_days']} дней."
    )


def schedule_next(chat_id: str, job_queue):
    cfg = get_user_settings(chat_id)
    if not cfg:
        return

    days = random.randint(cfg["min_days"], cfg["max_days"])
    secs = days * 24 * 3600
    job_name = f"gift_job_{chat_id}"

    # Убираем предыдущие
    for job in job_queue.get_jobs_by_name(job_name):
        job.schedule_removal()

    # Планируем новое
    job_queue.run_once(
        reminder,
        when=secs,
        name=job_name,
        data={"chat_id": chat_id},
    )

    # Логируем рассчитанное время старта
    run_at = datetime.now() + timedelta(seconds=secs)
    print(f"[GiftBot] Scheduled for {chat_id} at {run_at.strftime('%Y-%m-%d %H:%M:%S')}")


async def reminder(context: ContextTypes.DEFAULT_TYPE):
    chat = context.job.data["chat_id"]
    try:
        idea = provider.get_random_gift()
        await context.bot.send_message(chat_id=chat, text=f"🎁 {idea}")
    finally:
        schedule_next(chat, context.job_queue)


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setinterval", set_interval))
    app.add_handler(CommandHandler("showinterval", show_interval))

    for chat_id, _ in list_all_user_settings():
        schedule_next(chat_id, app.job_queue)

    print(f"python-telegram-bot v{ptb_version} is running...")
    app.run_polling()
