from aiogram.fsm.state import State, StatesGroup


class MakeNewPoint(StatesGroup):
    address_and_type = State()
