#!/usr/bin/env python3
import asyncio
from datetime import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from adapter.persistence.firestore_user_settings_repository import FirestoreUserSettingsRepository
from adapter.service.ai_gift_generator import OpenAIGiftGenerator
from adapter.service.default_schedule_determiner import DefaultScheduleDeterminer
from adapter.service.random_interval_calculator import RandomIntervalCalculator
from config.config_service import ConfigService
from config.environment_loader import EnvironmentLoader
from infrastructure.logging import logger as lgr
from infrastructure.openai.openai_service import OpenAIService
from infrastructure.persistence.firestore_service import FirestoreService
from infrastructure.scheduling.job_queue_manager import JobQueueManager
from infrastructure.telegram.telegram_service import TelegramService
from usecase.generate_now import GenerateNow
from usecase.initialize_user import InitializeUser
from usecase.send_gift import SendGift
from usecase.set_interval import SetInterval
from usecase.show_interval import ShowInterval
from usecase.startup_scheduler import StartupScheduler

# Initialize structured logging
logger = lgr.setup_logging()


# ---------------------- Handlers ----------------------
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = str(update.effective_chat.id)
    logger.info("Received /start from %s", chat_id)
    text = context.bot_data['init_uc'].execute(chat_id)
    await context.bot.send_message(chat_id=chat_id, text=text)


async def setinterval_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = str(update.effective_chat.id)
    args = context.args
    if len(args) != 2 or not all(arg.isdigit() for arg in args):
        await context.bot.send_message(
            chat_id=chat_id,
            text="Invalid format. Use: /setinterval <min_days> <max_days>"
        )
        return
    min_d, max_d = map(int, args)
    text = context.bot_data['set_interval_uc'].execute(chat_id, min_d, max_d)
    await context.bot.send_message(chat_id=chat_id, text=text)


async def showinterval_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = str(update.effective_chat.id)
    text = context.bot_data['show_interval_uc'].execute(chat_id)
    await context.bot.send_message(chat_id=chat_id, text=text)


async def generate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = str(update.effective_chat.id)
    logger.info("Received /generate from %s", chat_id)
    await context.bot_data['generate_now_uc'].execute(chat_id)


# Global error handler
async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Unhandled exception: %s", context.error)
    if isinstance(update, Update) and update.effective_chat:
        try:
            await context.bot.send_message(
                chat_id=str(update.effective_chat.id),
                text="An unexpected error occurred. Please try again later."
            )
        except Exception:
            logger.exception("Failed to notify user about the error.")


# ---------------------- Registration ----------------------
def register_handlers(app):
    """Register all command handlers in a DRY fashion."""
    cmds = {
        'start': start_handler,
        'setinterval': setinterval_handler,
        'showinterval': showinterval_handler,
        'generate': generate_handler,
    }
    for cmd, handler in cmds.items():
        app.add_handler(CommandHandler(cmd, handler))
    app.add_error_handler(global_error_handler)


# ---------------------- Main ----------------------
async def main() -> None:
    # Load config
    EnvironmentLoader.load()
    config = ConfigService()

    # Init infra
    fs_service = FirestoreService(
        credentials_path=config.firebase_credentials,
        project_id=config.firebase_project_id
    )
    repo = FirestoreUserSettingsRepository(fs_service)
    ai_service = OpenAIService(api_key=config.openai_key)
    tg_service = TelegramService(token=config.telegram_token)
    scheduler = JobQueueManager(timezone='UTC')

    # Domain services
    interval_calc = RandomIntervalCalculator()
    schedule_det = DefaultScheduleDeterminer()
    generate_gift = OpenAIGiftGenerator(ai_service)

    # Use cases
    init_uc = InitializeUser(repo, interval_calc, schedule_det, scheduler.schedule_at)
    set_interval_uc = SetInterval(repo, interval_calc, schedule_det, scheduler.schedule_at, scheduler.remove_job)
    show_interval_uc = ShowInterval(repo)
    send_gift_uc = SendGift(repo, generate_gift, tg_service, interval_calc, schedule_det,
                            scheduler.schedule_at)
    startup_uc = StartupScheduler(repo, interval_calc, schedule_det, scheduler.schedule_at)
    generate_now_uc = GenerateNow(generate_gift, tg_service)

    # Bind placeholders
    init_uc.send_placeholder = send_gift_uc.execute
    set_interval_uc.send_placeholder = send_gift_uc.execute
    startup_uc.send_placeholder = send_gift_uc.execute

    # Build Telegram app
    app = ApplicationBuilder().token(config.telegram_token).build()

    # Store use cases in context for handlers
    app._bot_data['init_uc'] = init_uc
    app._bot_data['set_interval_uc'] = set_interval_uc
    app._bot_data['show_interval_uc'] = show_interval_uc
    app._bot_data['generate_now_uc'] = generate_now_uc

    # Register handlers
    register_handlers(app)

    # Start scheduler
    scheduler.start()
    startup_uc.execute()

    logger.info("GiftBot started at %s UTC", datetime.utcnow().isoformat())
    await app.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
