from aiogram.fsm.state import State, StatesGroup


class TechHelp(StatesGroup):
    address = State()
    category = State()
    desc = State()
