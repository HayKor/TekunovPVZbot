from typing import List

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from callback.enums import AdminCallback
from database.engine import async_session
from database.point_crud import (
    create_point,
    delete_point,
    get_point,
    get_points,
)
from database.polls_crud import (
    create_poll,
    create_poll_answer,
    update_revision_id,
)
from database.revision_crud import create_revision, get_latest_revision
from database.user_crud import get_admin_list
from filters import IsAdmin
from keyboards.admin_keyboard import build_back_to_points_menu_kb
from keyboards.menu_keyboard import build_cancel_kb
from states.admin_states import DeletePoint, MakeNewPoint


router = Router(name=__name__)

# Global filters
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(Command("list_admins"))
async def handle_list_admins(message: types.Message) -> None:
    admin_list = await get_admin_list(async_session)
    text = "<b>Список всех администраторов:</b>\n"
    if admin_list:
        for admin in admin_list:
            text += (
                f"<b>ID:</b> {admin.id}, <b>nickname:</b> @{admin.nickname};\n"
            )
        await message.reply(text=text, parse_mode=ParseMode.HTML)
    else:
        await message.reply(text="Нету(((", parse_mode=ParseMode.HTML)


@router.message(Command("list_points"))
async def handle_list_points(message: types.Message) -> None:
    points_list = await get_points(async_session)
    text = "<b>Список всех пунктов:</b>\n"
    if points_list:
        for count, point in enumerate(points_list):
            text += f"<b>{count + 1}.</b> <code>{point.address} {point.type}</code>\n"
        await message.reply(text=text, parse_mode=ParseMode.HTML)
    else:
        await message.reply(text="Нету(((", parse_mode=ParseMode.HTML)


@router.message(Command("create_point"))
@router.callback_query(F.data == AdminCallback.POINTS_ADD)
async def handle_create_point(
    message: types.Message | types.CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(MakeNewPoint.address_and_type)
    text = "Пожалуйста, введите адреса новых пунктов и службу через пробел.\n"
    text += "Каждый пункт должен быть с новой строчки.\n"
    text += "Пожалуйста, пишите службу в таком формате: WB, OZON, ЯМ.\n"
    text += "Например, <code>Рокотова 5 OZON</code>."
    text += "Для отмены нажмите /cancel"
    if isinstance(message, types.Message):
        await message.reply(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=build_cancel_kb(),
        )
    else:
        await message.message.edit_text(  # type: ignore
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=build_back_to_points_menu_kb(),
        )


@router.message(MakeNewPoint.address_and_type, F.text)
async def process_create_address_and_type(
    message: types.Message, state: FSMContext
) -> None:
    points = message.text.split("\n")  # type: ignore
    text = "Добавленные пункты:\n\n"
    for point in points:
        point_raw = point.split()
        address, type = " ".join(point_raw[:-1]), point_raw[-1]
        check = await get_point(async_session, address, type)
        if check:
            text += f'Пункт "<b>{check.address} {check.type}</b>" уже есть!\n'
        else:
            point = await create_point(async_session, address, type)
            if point:
                text += f'Пункт "<b>{point.address} {point.type}</b>" успешно создан!\n'
            else:
                text += "Что-то пошло не так..."
    await message.reply(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=build_back_to_points_menu_kb(),
    )
    await state.clear()


@router.message(Command("delete_point"))
@router.callback_query(F.data == AdminCallback.POINTS_REMOVE)
async def handle_delete_point(
    message: types.Message | types.CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(DeletePoint.address_and_type)
    text = "Пожалуйста, введите адреса новых пунктов и службу через пробел.\n"
    text += "Каждый пункт должен быть с новой строчки.\n"
    text += "Пожалуйста, пишите службу в таком формате: WB, OZON, ЯМ.\n"
    text += "Например, <code>Рокотова 5 OZON</code>."
    text += "Для отмены нажмите /cancel"
    if isinstance(message, types.Message):
        await message.reply(
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=build_back_to_points_menu_kb(),
        )
    else:
        await message.message.edit_text(  # type: ignore
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=build_back_to_points_menu_kb(),
        )


@router.message(DeletePoint.address_and_type, F.text)
async def process_delete_address_and_type(
    message: types.Message, state: FSMContext
) -> None:
    points = message.text.split("\n")  # type: ignore
    text = "Удаленные пункты:\n\n"
    for point in points:
        point_raw = point.split()
        address, type = " ".join(point_raw[:-1]), point_raw[-1]
        check = await get_point(async_session, address, type)
        if not check:
            text += f'Пункта "{point}" нет!\n'
        else:
            point = await delete_point(async_session, address, type)
            if point:
                text += f'Пункт "<b>{point.address} {point.type}</b>" успешно удален!\n'
            else:
                text += "Что-то пошло не так..."
    await message.reply(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=build_back_to_points_menu_kb(),
    )
    await state.clear()


@router.message(Command("test"))
async def handle_test(message: types.Message) -> None:
    question_prefix = r"Отметьтесь в опросе о своем фактическом выезде на работу. (Если вы опаздываете, то отпишите ниже)"
    common_message = r"""Коллеги, доброе утро!
Ниже <b>отметьтесь</b> в опросе о своем фактическом выезде на работу, выбрав пункт, на котором вы сегодня работаете.
Если вы вдруг опаздываете, то ниже под опросом напишите: 'Рокотова. Опаздываю на 15 минут.'
Если за час до фактического открытия пункта вы не отпишитесь, то вам автоматически будет искаться <b>замена</b>."""
    await message.reply(
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
        poll = await message.bot.send_poll(  # type: ignore
            chat_id=message.chat.id,
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


@router.message(Command("show_attendance_info"))
async def handle_show_attendance_info(message: types.Message):
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

    await message.answer(
        text=text,
        parse_mode=ParseMode.HTML,
    )
