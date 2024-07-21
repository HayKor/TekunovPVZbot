from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database.engine import async_session
from database.user_crud import (
    get_user_by_nickname,
    make_user_admin,
    make_user_not_admin,
)
from filters import IsFather
from states.father_states import MakeNewAdminForm, RemoveAdminForm


router = Router(
    name=__name__,
)


@router.message(Command("assign_admin"), IsFather())
async def handle_assign_new_admin(message: types.Message, state: FSMContext) -> None:
    await state.set_state(MakeNewAdminForm.user_nickname)
    await message.reply(
        text="Введите никнейм юзера без @, кого вы хотите назначить администратором."
    )


@router.message(MakeNewAdminForm.user_nickname)
async def process_user_id(message: types.Message, state: FSMContext) -> None:
    user = await get_user_by_nickname(async_session, user_nickname=message.text)
    if user:
        if user.is_admin:
            await message.reply(text=f"Юзер {message.text} уже администратор!")
        if not user.is_admin:
            await make_user_admin(async_session, user_id=user.id)
            await message.reply(
                text=f"Юзер {message.text} успешно назначен администратором!"
            )
    else:
        await message.reply(
            text="Такой юзер не найден! Пожалуйста, убедитесь, что Вы ввели никнейм без @"
        )
    await state.clear()


@router.message(Command("remove_admin"), IsFather())
async def handle_remove_admin(message: types.Message, state: FSMContext) -> None:
    await state.set_state(RemoveAdminForm.admin_nicknaname)
    await message.reply(
        text="Введите id администратора, кого вы хотите снять с должности."
    )


@router.message(RemoveAdminForm.admin_nicknaname)
async def process_admin_id(message: types.Message, state: FSMContext) -> None:
    user = await get_user_by_nickname(async_session, user_nickname=message.text)
    if user:
        if not user.is_admin:
            await message.reply(text=f"Юзер {message.text} не администратор!")
        if user.is_admin:
            await make_user_not_admin(async_session, user.id)
            await message.reply(text=f"Админ {message.text} снят с администрирования!")
    else:
        await message.reply(text=f"Юзер {message.text} не найден!..")
    await state.clear()
