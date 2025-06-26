#!/usr/bin/env python3
from datetime import datetime

from telegram.ext import ApplicationBuilder, CommandHandler

from adapter.persistence.firestore_user_settings_repository import FirestoreUserSettingsRepository
from adapter.service.ai_gift_generator import OpenAIGiftGenerator
from adapter.service.default_schedule_determiner import DefaultScheduleDeterminer
from adapter.service.random_interval_calculator import RandomIntervalCalculator
from config.config_service import ConfigService
from config.environment_loader import EnvironmentLoader
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

# 1. Загрузка окружения
EnvironmentLoader.load()
config = ConfigService()

# 2. Инициализация инфраструктуры
fs_service = FirestoreService(
    credentials_path=config.firebase_credentials,
    project_id=config.firebase_project_id
)
repo = FirestoreUserSettingsRepository(fs_service)
ai_service = OpenAIService(api_key=config.openai_key)
telegram_service = TelegramService(token=config.telegram_token)
scheduler = JobQueueManager(timezone='UTC')

# 3. Реализации доменных сервисов
interval_calc = RandomIntervalCalculator()
schedule_det = DefaultScheduleDeterminer()

# 4. Инициализация use case
init_user_uc = InitializeUser(
    repository=repo,
    interval_calculator=interval_calc,
    schedule_determiner=schedule_det,
    schedule_at=scheduler.schedule_at
)
set_interval_uc = SetInterval(
    repository=repo,
    interval_calculator=interval_calc,
    schedule_determiner=schedule_det,
    schedule_at=scheduler.schedule_at,
    remove_job=scheduler.remove_job
)
show_interval_uc = ShowInterval(repository=repo)
send_gift_uc = SendGift(
    repository=repo,
    gift_generator=OpenAIGiftGenerator(ai_service),
    telegram_service=telegram_service,
    interval_calculator=interval_calc,
    schedule_determiner=schedule_det,
    schedule_at=scheduler.schedule_at
)
startup_sched_uc = StartupScheduler(
    repository=repo,
    interval_calculator=interval_calc,
    schedule_determiner=schedule_det,
    schedule_at=scheduler.schedule_at
)
generate_now_uc = GenerateNow(
    gift_generator=OpenAIGiftGenerator(ai_service),
    telegram_service=telegram_service
)

# 5. Настройка Telegram-бота
app = ApplicationBuilder().token(config.telegram_token).build()


async def start_handler(update, context):
    chat_id = str(update.effective_chat.id)
    text = init_user_uc.execute(chat_id)
    await context.bot.send_message(chat_id=chat_id, text=text)


async def setinterval_handler(update, context):
    chat_id = str(update.effective_chat.id)
    args = context.args

    # Если аргументов нет или их не два — сразу отписаться об ошибке
    if len(args) != 2 or not all(arg.isdigit() for arg in args):
        await context.bot.send_message(
            chat_id=chat_id,
            text="Неверный формат. Используй:\n/setinterval <мин_дней> <макс_дней>"
        )
        return

    # Теперь безопасно парсим числа
    min_d, max_d = map(int, args)
    text = set_interval_uc.execute(chat_id, min_d, max_d)
    await context.bot.send_message(chat_id=chat_id, text=text)


async def showinterval_handler(update, context):
    chat_id = str(update.effective_chat.id)
    text = show_interval_uc.execute(chat_id)
    await context.bot.send_message(chat_id=chat_id, text=text)


async def generate_handler(update, context):
    chat_id = str(update.effective_chat.id)
    await generate_now_uc.execute(chat_id)


app.add_handler(CommandHandler('start', start_handler))
app.add_handler(CommandHandler('setinterval', setinterval_handler))
app.add_handler(CommandHandler('showinterval', showinterval_handler))
app.add_handler(CommandHandler('generate', generate_handler))

# 6. Запуск планировщика и перепланирование существующих задач
scheduler.start()
startup_sched_uc.execute()

# 7. Запуск бота
print(f"GiftBot started at {datetime.utcnow()} UTC")
app.run_polling()
