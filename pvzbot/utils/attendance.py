from typing import TYPE_CHECKING

from aiogram.enums import ParseMode
from config import config
from database.engine import async_session
from database.point_crud import get_points
from database.polls_crud import create_poll, create_poll_answer
from database.revision_crud import create_revision, get_latest_revision


if TYPE_CHECKING:
    from typing import List

    from aiogram import Bot


async def schedule_show_attendance_info(bot: Bot):
    revision = await get_latest_revision(async_session)
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
                ):
                    text += f"{count}. {poll_answer.question} <b>не отметился в опросе</b>\n"
                    count += 1

    await bot.send_message(
        chat_id=config.pvz_attendance_chat_id,
        text=text,
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
    points = [points[i : i + 9] for i in range(0, len(points), 9)]  # type: ignore
    polls_list = []

    for points_part in points:
        question_options: List = [
            f"{point.address} {point.type}" for point in points_part
        ]
        question_options.append("Посмотреть результаты")
        poll = await bot.send_poll(  # type: ignore
            chat_id=config.pvz_chat_id,
            question=question_prefix,
            options=question_options,
            type="regular",
            is_anonymous=False,
        )
        poll_id = poll.poll.id  # type: ignore

        # Создание записей в таблице poll_answers
        await create_poll(async_session, poll_id=poll_id)  # type: ignore
        for idx, poll_answer in enumerate(question_options):
            await create_poll_answer(
                async_session,
                poll_id=poll_id,  # type: ignore
                question=poll_answer,
                option_id=idx,
            )
        polls_list.append(str(poll_id))

    # Создание ревизии и приписание ее номера записям в polls
    revision = await create_revision(async_session)
    for poll in polls_list:
        await update_revision_id(async_session, poll, revision.id)  # type: ignore
