from typing import List, Literal

from aiogram import Bot
from aiogram.enums import ParseMode
from config import config
from database.engine import async_session
from database.point_crud import get_points
from database.polls_crud import (
    create_poll,
    create_poll_answer,
    update_revision_id,
)
from database.revision_crud import create_revision, get_latest_revision
from utils.sheets.attendance import get_workers_dict
from utils.sheets.client import gc as g_client


async def schedule_show_attendance_info(
    bot: Bot, worktime: Literal["10:00", "9:00"]
):
    revision = await get_latest_revision(async_session)
    try:
        points_workers_dict = get_workers_dict(
            g_client=g_client,
            date=str(revision.date),
        )
    except:
        points_workers_dict = {}
    not_attended_list = []

    text = "Эти пункты не отметились в опросе:\n\n"
    if revision is None:
        text += "Something went wrong, пожалуйста будьте пациентами"
    else:
        count = 1
        for poll in revision.polls:
            for poll_answer in poll.poll_answers:
                if (
                    poll_answer.is_answered == False
                    and poll_answer.question != "Посмотреть результаты"
                    and poll_answer.question.split()[-1] == worktime
                ):
                    text += f"{count}. {poll_answer.question} <b>не отметился в опросе</b>\n"
                    count += 1
                    not_attended_list.append(
                        " ".join(poll_answer.question.split()[:-1])
                    )

    await bot.send_message(
        chat_id=config.pvz_attendance_chat_id,
        text=text,
        parse_mode=ParseMode.HTML,
    )

    not_attended_text = ""
    for point in not_attended_list:
        not_attended_text += (
            f"{points_workers_dict.get(point, 'No name')} - {point}\n"
        )

    await bot.send_message(
        chat_id=config.pvz_attendance_chat_id,
        text=not_attended_text,
        parse_mode=ParseMode.HTML,
    )


async def send_attendance_poll(bot: Bot) -> None:
    question_prefix = r"Отметьтесь в опросе о своем фактическом выезде на работу. (Если вы опаздываете, то отпишите ниже)"
    common_message = r"""Коллеги, доброе утро!
Ниже <b>отметьтесь</b> в опросе о своем фактическом выезде на работу, выбрав пункт, на котором вы сегодня работаете.
Если вы вдруг опаздываете, то ниже под опросом напишите: 'Рокотова. Опаздываю на 15 минут.'
Если за час до фактического открытия пункта вы не отпишитесь, то вам автоматически будет искаться <b>замена</b>."""
    await bot.send_message(
        chat_id=config.pvz_chat_id,
        text=common_message,
        parse_mode=ParseMode.HTML,
    )

    # Получить список опросов и разбить его на равные группы по 9 пунктов
    points = await get_points(async_session)
    points = [points[i : i + 9] for i in range(0, len(points), 9)]
    polls_list = []

    for points_part in points:
        question_options: List = [
            f"{point.address} {point.type} {point.worktime}"
            for point in points_part
        ]
        question_options.append("Посмотреть результаты")
        poll = await bot.send_poll(
            chat_id=config.pvz_chat_id,
            question=question_prefix,
            options=question_options,
            type="regular",
            is_anonymous=False,
        )
        poll_id: int = poll.poll.id

        await create_poll(async_session, poll_id=poll_id)

        # Создание записей в таблице poll_answers
        for idx, poll_answer in enumerate(question_options):
            await create_poll_answer(
                async_session,
                poll_id=poll_id,
                question=poll_answer,
                option_id=idx,
            )
        polls_list.append(poll_id)

    # Создание ревизии и приписание ее номера записям в polls
    revision = await create_revision(async_session)
    for poll in polls_list:
        await update_revision_id(async_session, poll, revision.id)
