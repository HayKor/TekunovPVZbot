from aiogram.fsm.state import State, StatesGroup


class MakeNewAdminForm(StatesGroup):
    user_nickname = State()


class RemoveAdminForm(StatesGroup):
    admin_nicknaname = State()
