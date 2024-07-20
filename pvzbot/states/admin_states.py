from aiogram.fsm.state import State, StatesGroup


class MakeNewPoint(StatesGroup):
    address = State()
    type = State()
