from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database.engine import async_session
from database.point_crud import (
    create_point,
    delete_point,
    get_point,
    get_points,
)
from database.user_crud import get_admin_list
from filters import IsAdmin
from states.admin_states import DeletePoint, MakeNewPoint


router = Router(name=__name__)


@router.message(Command("list_admins"), IsAdmin())
async def handle_list_admins(message: types.Message) -> None:
    admin_list = await get_admin_list(async_session)
    text = "<b>Список всех администраторов:</b>\n"
    if admin_list:
        for admin in admin_list:
            text += f"<b>ID:</b> {admin.id}, <b>nickname:</b> @{admin.nickname};\n"
        await message.reply(text=text, parse_mode=ParseMode.HTML)
    else:
        await message.reply(text="Нету(((", parse_mode=ParseMode.HTML)


@router.message(Command("list_points"), IsAdmin())
async def handle_list_points(message: types.Message) -> None:
    points_list = await get_points(async_session)
    text = "<b>Список всех пунктов:</b>\n"
    if points_list:
        for count, point in enumerate(points_list):
            text += f"<b>{count + 1}.</b> <code>{point.address} {point.type}</code>\n"
        await message.reply(text=text, parse_mode=ParseMode.HTML)
    else:
        await message.reply(text="Нету(((", parse_mode=ParseMode.HTML)


@router.message(Command("create_point"), IsAdmin())
async def handle_create_point(message: types.Message, state: FSMContext) -> None:
    await state.set_state(MakeNewPoint.address_and_type)
    text = "Пожалуйста, введите адреса новых пунктов и службу через пробел.\n"
    text += "Каждый пункт должен быть с новой строчки.\n"
    text += "Пожалуйста, пишите службу в таком формате: WB, OZON, ЯМ.\n"
    text += "Например, <code>Рокотова 5 OZON</code>."
    text += "Для отмены нажмите /cancel"
    await message.reply(text=text, parse_mode=ParseMode.HTML)


@router.message(MakeNewPoint.address_and_type, F.text)
async def process_create_address_and_type(
    message: types.Message, state: FSMContext
) -> None:
    points = message.text.split("\n")
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
                text += f"Что-то пошло не так..."
    await message.reply(text=text, parse_mode=ParseMode.HTML)
    await state.clear()


@router.message(Command("delete_point"), IsAdmin())
async def handle_delete_point(message: types.Message, state: FSMContext) -> None:
    await state.set_state(DeletePoint.address_and_type)
    text = "Пожалуйста, введите адреса новых пунктов и службу через пробел.\n"
    text += "Каждый пункт должен быть с новой строчки.\n"
    text += "Пожалуйста, пишите службу в таком формате: WB, OZON, ЯМ.\n"
    text += "Например, <code>Рокотова 5 OZON</code>."
    text += "Для отмены нажмите /cancel"
    await message.reply(text=text, parse_mode=ParseMode.HTML)


@router.message(DeletePoint.address_and_type, F.text)
async def process_delete_address_and_type(
    message: types.Message, state: FSMContext
) -> None:
    points = message.text.split("\n")
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
                text += f"Что-то пошло не так..."
    await message.reply(text=text, parse_mode=ParseMode.HTML)
    await state.clear()
