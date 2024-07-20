from aiogram import types
from aiogram.filters import Filter
from database.database import get_user_by_id
from database.engine import async_session
from database.models import Users


# TODO
class IsFather(Filter):
    async def __call__(self, message: types.Message) -> bool:
        user = await get_user_by_id(async_session, message.from_user.id)
        return user.is_father


class IsAdmin(Filter):
    async def __call__(self, message: types.Message) -> bool:
        user = await get_user_by_id(async_session, message.from_user.id)
        return user.is_admin
