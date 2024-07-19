from aiogram import Router, types
from aiogram.filters import Command


router = Router(name=__name__)


@router.message(Command("start"))
async def handle_start(message: types.Message):
    pass
