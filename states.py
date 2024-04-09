from aiogram.fsm.state import State, StatesGroup


class InfoStates(StatesGroup):
    CHOOSE_MAP = State()
    CHOOSE_TEAM = State()
    CHOOSE_INFO = State()
    CHOOSE_POSITION = State()
    POSITION_DESCRIPTION = State()


class AddItemStates(StatesGroup):
    ADD_PLACE = State()
    ADD_PHOTO = State()
    ADD_DESCRIPTION = State()
    ADD_NUMBER = State()
