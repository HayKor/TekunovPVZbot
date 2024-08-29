from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.attendance import schedule_show_attendance_info, send_attendance_poll


scheduler = AsyncIOScheduler()


def set_scheduled_jobs(bot: Bot) -> None:
    scheduler.add_job(
        send_attendance_poll,
        "cron",
        hour=4,
        minute=15,
        args=(bot,),
    )
    scheduler.add_job(
        schedule_show_attendance_info,
        "cron",
        hour=5,
        minute=10,
        args=(bot, "9:00"),
    )
    scheduler.add_job(
        schedule_show_attendance_info,
        "cron",
        hour=6,
        minute=10,
        args=(bot, "10:00"),
    )
