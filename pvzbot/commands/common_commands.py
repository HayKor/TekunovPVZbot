from aiogram import Router, types
from aiogram.filters import Command
from database.database import create_user
from database.engine import async_session


router = Router(name=__name__)


@router.message(Command("start"))
async def handle_start(message: types.Message):
    user = await create_user(
        async_session,
        id=message.from_user.id,
        nickname=message.from_user.username,
    )
    if not user:
        await message.reply(
            text="Привет, ты успешно зарегистрирован в нашей Базе Данных!",
        )
    else:
        await message.reply(
            text="Привет! Ты уже зарегистрирован в Базе Данных!",
        )
