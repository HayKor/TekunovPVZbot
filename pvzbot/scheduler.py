from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()


async def send_attendance_poll(bot: Bot) -> None:
    question_prefix = r"Отметьтесь в опросе о своем фактическом выезде на работу. (Если вы опаздываете, то отпишите ниже)"
    common_message = r"""Коллеги, доброе утро\!
Ниже **отметьтесь** в опросе о своем фактическом выезде на работу, выбрав пункт, на котором вы сегодня работаете\.
Если вы вдруг опаздываете, то ниже под опросом напишите: 'Рокотова\. Опаздываю на 15 минут\.'
Если за час до фактического открытия пункта вы не отпишитесь, то вам автоматически будет искаться замена\."""


def set_scheduled_jobs(bot: Bot) -> None:
    scheduler.add_job(
        send_attendance_poll,
        "cron",
        hour=7,
        minute=30,
        args=(bot,),
    )
