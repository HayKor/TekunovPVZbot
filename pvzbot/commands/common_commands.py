from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown
from database.engine import async_session
from database.user_crud import create_user, get_user_by_id


router = Router(name=__name__)


@router.message(Command("start"))
async def handle_start(message: types.Message):
    url = "https://anti-maidan.com/wp-content/uploads/2023/07/terminator-stanovitsja-realnostjunbsp-shvarcenegger-92e05be.webp"
    user = await get_user_by_id(
        async_session,
        user_id=message.from_user.id,
    )
    if not user:
        await create_user(
            async_session, message.from_user.id, message.from_user.username
        )
        await message.reply(
            text=f"{markdown.hide_link(url=url)}Привет, я - бот-помощник <b>ИП Текунов</b>! Чтобы узнать про функционал - введите /help",
            parse_mode=ParseMode.HTML,
        )
    else:
        await message.reply(
            text=f"{markdown.hide_link(url=url)}Привет, мы уже знакомы! Узнать про функционал - /help",
            parse_mode=ParseMode.HTML,
        )


@router.message(Command("cancel"))
async def handle_cancel(message: types.Message, state: FSMContext) -> None:
    await message.reply(
        text="Предыдущее действие отменено успешно.",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.clear()


@router.message(Command("get_chat_id"))
async def handle_get_chat_id(message: types.Message) -> None:
    await message.reply(str(message.chat.id))
