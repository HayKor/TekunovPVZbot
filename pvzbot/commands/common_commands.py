from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database.engine import async_session
from database.user_crud import create_user


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


@router.message(Command("cancel"))
async def handle_cancel(message: types.Message, state: FSMContext) -> None:
    await message.reply(text="Предыдущее действие отменено успешно.")
    await state.clear()


@router.message()
async def handle_any(message: types.Message) -> None:
    await message.reply(text="У вас нету прав в этом боте((((\nНапишите @haykorarthur")
