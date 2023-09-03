from aiogram.fsm.state import StatesGroup, State


class PurchaseState(StatesGroup):
    waiting_for_price = State()
    waiting_reply = State()
