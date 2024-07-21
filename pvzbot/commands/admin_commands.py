from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database.engine import async_session
from database.point_crud import create_point, get_point, get_points
from database.user_crud import get_admin_list
from filters import IsAdmin
from states.admin_states import MakeNewPoint


router = Router(name=__name__)


@router.message(Command("list_admins"), IsAdmin())
async def handle_list_admins(message: types.Message) -> None:
    admin_list = await get_admin_list(async_session)
    text = f"<b>Список всех администраторов:</b>\n"
    if admin_list:
        for admin in admin_list:
            text += f"<b>ID:</b> {admin.id}, <b>nickname:</b> @{admin.nickname};\n"
        await message.reply(text=text, parse_mode=ParseMode.HTML)
    else:
        await message.reply(text="Нету(((", parse_mode=ParseMode.HTML)


@router.message(Command("list_points"), IsAdmin())
async def handle_list_points(message: types.Message) -> None:
    points_list = await get_points(async_session)
    text = f"<b>Список всех пунктов:</b>\n"
    if points_list:
        for count, point in enumerate(points_list):
            text += f"<b>{count + 1}.</b> {point.address} {point.type}\n"
        await message.reply(text=text, parse_mode=ParseMode.HTML)
    else:
        await message.reply(text="Нету(((", parse_mode=ParseMode.HTML)


@router.message(Command("create_point"), IsAdmin())
async def handle_create_admin(message: types.Message, state: FSMContext) -> None:
    await state.set_state(MakeNewPoint.address_and_type)
    text = "Пожалуйста, введите адрес нового пункта и службу через пробел.\n"
    text += "Пожалуйста, пишите службу в таком формате: WB, OZON, ЯМ.\n"
    text += "Например, <code>Рокотова 5 OZON</code>."
    await message.reply(text=text, parse_mode=ParseMode.HTML)


@router.message(MakeNewPoint.address_and_type)
async def process_address_and_type(message: types.Message, state: FSMContext) -> None:
    point_raw = message.text.split()
    address, type = " ".join(point_raw[:-1]), point_raw[-1]
    check = await get_point(async_session, address, type)
    if check:
        await message.reply(
            f"Такой пункт уже есть! <b>{check.address} {check.type}</b>",
            parse_mode=ParseMode.HTML,
        )
    else:
        point = await create_point(async_session, address, type)
        if point:
            await message.reply(
                f'Пункт "<b>{point.address} {point.type}</b>" успешно создан!',
                parse_mode=ParseMode.HTML,
            )
        else:
            await message.reply(text="Что-то пошло не так...")
    await state.clear()
