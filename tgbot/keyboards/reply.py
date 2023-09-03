from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

registration_button = [
    [KeyboardButton(text="Зарегестрироваться")]
]

registration_keyboard = ReplyKeyboardMarkup(
    keyboard=registration_button, resize_keyboard=True,
    one_time_keyboard=True, input_field_placeholder='Зарегестрироваться')

donation_button = [
    [KeyboardButton(text="Пожертвовать")]
]

donation_keyboard = ReplyKeyboardMarkup(
    keyboard=donation_button, resize_keyboard=True,
    one_time_keyboard=True, input_field_placeholder='Пожертвовать')

