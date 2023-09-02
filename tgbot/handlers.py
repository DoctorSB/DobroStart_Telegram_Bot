
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext



admin_router = Router()


@admin_router.message(Command("start"))
async def sure(message: Message, state: FSMContext):
    await message.answer(text='Running',)
