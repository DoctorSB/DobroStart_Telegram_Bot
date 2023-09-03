from aiogram.filters.callback_data import CallbackData


class PriceCallbackFactory(CallbackData, prefix="price"):
    action: str
