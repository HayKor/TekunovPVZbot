from aiogram import Router, types
from aiogram.filters import Command
from database.database import make_user_admin
from database.engine import async_session


router = Router(name=__name__)


@router.message(Command("assign_new_admin"))
async def handle_assign_new_admin(message: types.Message) -> None:
    pass
