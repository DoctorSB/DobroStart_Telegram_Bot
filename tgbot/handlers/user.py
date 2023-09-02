from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types.web_app_info import WebAppInfo

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Вітаю, звичайний користувач!", web_app=WebAppInfo())
