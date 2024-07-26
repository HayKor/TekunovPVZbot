from aiogram import Bot
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import config
from database.engine import async_session
from database.point_crud import get_points


scheduler = AsyncIOScheduler()


async def send_attendance_poll(bot: Bot) -> None:
    question_prefix = r"Отметьтесь в опросе о своем фактическом выезде на работу. (Если вы опаздываете, то отпишите ниже)"
    common_message = r"""Коллеги, доброе утро!
Ниже <b>отметьтесь</b> в опросе о своем фактическом выезде на работу, выбрав пункт, на котором вы сегодня работаете.
Если вы вдруг опаздываете, то ниже под опросом напишите: 'Рокотова. Опаздываю на 15 минут.'
Если за час до фактического открытия пункта вы не отпишитесь, то вам автоматически будет искаться <b>замена</b>."""

    # Sendin message before polls
    await bot.send_message(
        chat_id=config.pvz_chat_id, text=common_message, parse_mode=ParseMode.HTML
    )

    points = await get_points(async_session)
    points = [points[i : i + 9] for i in range(0, len(points), 9)]
    for points_part in points:
        question_options = [f"{point.address} {point.type}" for point in points_part]
        question_options.append("Посмотреть результаты")
        await bot.send_poll(
            chat_id=config.pvz_chat_id,
            question=question_prefix,
            options=question_options,
            type="regular",
            is_anonymous=False,
        )


def set_scheduled_jobs(bot: Bot) -> None:
    pass
    # scheduler.add_job(
    #     send_attendance_poll,
    #     "interval",
    #     seconds=5,
    #     args=(bot,),
    # )
    scheduler.add_job(
        send_attendance_poll,
        "cron",
        hour=20,
        minute=45,
        args=(bot,),
    )
