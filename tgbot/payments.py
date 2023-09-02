from aiogram.filters import CommandStart, Command
from aiogram.types import LabeledPrice
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery, PreCheckoutQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.types.message import ContentType
from messages import MESSAGES

from config import  PAYMENTS_TOKEN
class PurchaseState(StatesGroup):
    waiting_for_price = State()
class PriceCallbackFactory(CallbackData, prefix="price"):
    action: str



payment_router = Router()
state = PurchaseState()

from main import bot


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





@payment_router.message(Command("buy"))
async def buy_process(message: Message, state: FSMContext):
    await state.set_state(PurchaseState.waiting_for_price)
    await message.answer("Выберите цену:", reply_markup=get_keyboard_sure())


@payment_router.callback_query(PurchaseState.waiting_for_price, PriceCallbackFactory.filter(F.action == '100'))
async def payment_one(callback: CallbackQuery,
                        callback_data: PriceCallbackFactory, state: FSMContext):
    price = int(callback.data.split(":")[1]) * 100
    prices = [LabeledPrice(label='Товар', amount=price)]
    await bot.send_invoice(
        callback.from_user.id,
        title='Товар',
        description='Описание товара',
        provider_token=PAYMENTS_TOKEN,
        currency='rub',
        prices=prices,
        start_parameter='example',
        payload='some_invoice'
    )
    await state.clear()
    await bot.answer_callback_query(callback.id)

@payment_router.pre_checkout_query(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@payment_router.message(F(ContentType.SUCCESSFUL_PAYMENT))
async def successful_payment(message: Message):
    await bot.send_message(
        message.chat.id,
        MESSAGES['successful_payment'].format(total_amount=message.successful_payment.total_amount // 100,
                                              currency=message.successful_payment.currency)
    )

