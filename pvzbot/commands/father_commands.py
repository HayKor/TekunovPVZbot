from aiogram import Router, types
from aiogram.filters import Command
from database.database import make_user_admin
from database.engine import async_session
from filters import IsFather


router = Router(name=__name__)


@router.message(Command("assign_new_admin"), IsFather())
async def handle_assign_new_admin(message: types.Message) -> None:
    await message.reply(text="Вы -- отец этого бота!")
