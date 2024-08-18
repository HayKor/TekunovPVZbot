from typing import TYPE_CHECKING

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.attendance import schedule_show_attendance_info, send_attendance_poll


if TYPE_CHECKING:
    from aiogram import Bot

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
        minute=0,
        args=(bot,),
    )
    scheduler.add_job(
        schedule_show_attendance_info,
        "cron",
        hour=6,
        minute=0,
        args=(bot,),
    )
