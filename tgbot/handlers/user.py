from aiogram import Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import LabeledPrice
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from tgbot.keyboards.inline import get_keyboard_sure
from tgbot.config import load_config
from tgbot.models.states import PurchaseState
from aiogram.types.message import ContentType
from aiogram.filters import CommandStart
from tgbot.filters.user import PriceCallbackFactory


config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("юзерка")


@user_router.message(Command("buy"))
async def buy_process(message: Message, state: FSMContext):
    await state.set_state(PurchaseState.waiting_for_price)
    await message.answer("Выберите цену:", reply_markup=get_keyboard_sure())


@user_router.callback_query(PurchaseState.waiting_for_price, PriceCallbackFactory.filter(F.action == '100'))
async def payment_one(callback: CallbackQuery,
                      callback_data: PriceCallbackFactory, state: FSMContext):
    price = int(callback.data.split(":")[1]) * 100
    prices = [LabeledPrice(label='Товар', amount=price)]
    await bot.send_invoice(
        callback.from_user.id,
        title='Товар',
        description='Описание товара',
        provider_token=config.tg_bot.payment_token,
        currency='rub',
        prices=prices,
        start_parameter='example',
        payload='some_invoice'
    )
    await state.clear()
    await bot.answer_callback_query(callback.id)


@user_router.pre_checkout_query(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@user_router.message(F(ContentType.SUCCESSFUL_PAYMENT))
async def successful_payment(message: Message):
    await message.answer(f'Спасибо за покупку! {message.successful_payment.total_amount // 100} {message.successful_payment.currency}')
