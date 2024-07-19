import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from commands import router as commands_router
from config import config


bot = Bot(
    token=config.bot_token,
)
dp = Dispatcher()
dp.include_router(commands_router)


async def send_attendance_poll(bot: Bot):
    question_prefix = r"Отметьтесь в опросе о своем фактическом выезде на работу. (Если вы опаздываете, то отпишите ниже)"
    common_message = r"""Коллеги, доброе утро\!
Ниже **отметьтесь** в опросе о своем фактическом выезде на работу, выбрав пункт, на котором вы сегодня работаете\.
Если вы вдруг опаздываете, то ниже под опросом напишите: 'Рокотова\. Опаздываю на 15 минут\.'
Если за час до фактического открытия пункта вы не отпишитесь, то вам автоматически будет искаться замена\."""

    await bot.send_message(
        chat_id=config.father_chat_id,
        text=common_message,
        parse_mode=ParseMode.MARKDOWN_V2,
    )

    await bot.send_poll(
        chat_id=config.father_chat_id,
        question=question_prefix,
        type="regular",
        options=[
            "A",
            "B",
            "C",
        ],
        is_anonymous=False,
    )


def set_scheduled_jobs(scheduler: AsyncIOScheduler, bot: Bot, *args, **kwargs):
    scheduler.add_job(
        send_attendance_poll,
        "cron",
        hour=7,
        minute=30,
        args=(bot,),
    )


async def main():
    logging.basicConfig(
        level=logging.INFO,
    )
    sched = AsyncIOScheduler()
    set_scheduled_jobs(scheduler=sched, bot=bot)

    try:
        sched.start()  # START BEFORE POLLING
        await dp.start_polling(bot)

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
