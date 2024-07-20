from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from database.database import get_admin_list, get_points
from database.engine import async_session
from filters import IsAdmin


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
            text += f"{count}. {point.address} {point.type}\n"
        await message.reply(text=text, parse_mode=ParseMode.HTML)
    else:
        await message.reply(text="Нету(((", parse_mode=ParseMode.HTML)
