from aiogram.fsm.state import State, StatesGroup


class MakeNewPoint(StatesGroup):
    address_and_type = State()


class DeletePoint(StatesGroup):
    address_and_type = State()


class AddOfficeEntity(StatesGroup):
    name = State()
    tg_nickname = State()
    phone = State()
    schedule = State()
    description = State()


class RemoveOfficeEntity(StatesGroup):
    number = State()
