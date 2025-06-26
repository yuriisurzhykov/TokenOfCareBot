from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger


class JobQueueManager:
    """
    Менеджер задач для отложенного выполнения функций.
    """

    def __init__(self, timezone: str = 'UTC'):
        self.scheduler = AsyncIOScheduler(timezone=timezone)

    def schedule_at(self, job_id: str, run_time: datetime, func, *args, **kwargs) -> None:
        """
        Планирует выполнение func в момент run_time.
        При совпадении job_id существующая задача заменяется.
        """
        trigger = DateTrigger(run_date=run_time)
        self.scheduler.add_job(
            func,
            trigger=trigger,
            id=job_id,
            args=args,
            kwargs=kwargs,
            replace_existing=True,
        )

    def schedule_in(self, job_id: str, delay_seconds: float, func, *args, **kwargs) -> None:
        """
        Планирует выполнение func через delay_seconds секунд от текущего момента.
        """
        run_time = datetime.utcnow() + timedelta(seconds=delay_seconds)
        self.schedule_at(job_id, run_time, func, *args, **kwargs)

    def remove_job(self, job_id: str) -> None:
        """
        Удаляет задачу по её идентификатору.
        """
        try:
            self.scheduler.remove_job(job_id)
        except Exception:
            pass

    def start(self) -> None:
        """
        Запускает планировщик (должен вызываться один раз при старте приложения).
        """
        self.scheduler.start()
