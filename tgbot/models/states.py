from aiogram.fsm.state import StatesGroup, State


class PurchaseState(StatesGroup):
    waiting_for_price = State()
    waiting_reply = State()


class UserState(StatesGroup):
    get_name = State()
    get_phone = State()
    get_email = State()
    access = State()
    access_denied = State()
    auntificatet = State()