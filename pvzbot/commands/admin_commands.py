from aiogram import Router, types
from aiogram.filters import Command
from database.database import get_admin_list
from database.engine import async_session
from filters import IsAdmin


router = Router(name=__name__)


@router.message(Command("list_admins"), IsAdmin())
async def handle_list_admins(message: types.Message) -> None:
    admin_list = await get_admin_list(async_session)
    text = f"Список всех администраторов:\n"
    if admin_list:
        for admin in admin_list:
            text += f"User id: {admin.id}, nickname: @{admin.nickname}\n"
        await message.reply(text=text)
    else:
        await message.reply(text="Нету(((")
