from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.filters.user import PriceCallbackFactory


def get_keyboard_sure():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="100", callback_data=PriceCallbackFactory(action="100")
    )
    builder.button(
        text="200", callback_data=PriceCallbackFactory(action="200")
    )

    builder.adjust(2)
    return builder.as_markup()


acces_button = [
    [InlineKeyboardButton(text="✅", callback_data="access")],
]

acces_keyboard = InlineKeyboardMarkup(inline_keyboard=acces_button)
