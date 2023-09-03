from aiogram import Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import LabeledPrice
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext


from tgbot.keyboards.inline import get_keyboard_sure, acces_keyboard
from tgbot.keyboards.reply import registration_keyboard, donation_keyboard
from tgbot.config import load_config
from tgbot.models.states import PurchaseState, UserState
from aiogram.types.message import ContentType
from aiogram.filters import CommandStart
from tgbot.filters.user import PriceCallbackFactory

import pandas as pd


config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')




user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, state: FSMContext):
    await message.reply("Привет! Я бот который ...", reply_markup=registration_keyboard)
    await state.set_state(UserState.get_name)


@user_router.message(F.text == "Зарегестрироваться" and UserState.get_name)
async def user_registration(message: Message, state: FSMContext):
    await message.answer("Введите ваше ФИО:")
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(UserState.get_phone)


@user_router.message(UserState.get_phone)
async def user_registration(message: Message, state: FSMContext):
    await message.answer("Введите ваш номер телефона:")
    await state.update_data(user_name=message.text)
    await state.set_state(UserState.get_email)


@user_router.message(UserState.get_email)
async def user_registration(message: Message, state: FSMContext):
    await state.set_state(UserState.access)
    await message.answer("Введите ваш email:")
    await state.update_data(user_phone=message.text)


@user_router.message(UserState.access)
async def user_registration(message: Message, state: FSMContext):
    await state.update_data(user_email=message.text)
    info = await state.get_data()
    await message.answer(f'Ваше имя: {info["user_name"]}\nВаш номер телефона: {info["user_phone"]}\nВаш email: {info["user_email"]}\nДаете согласие на обработку персональных данных?', reply_markup=acces_keyboard)
    await state.set_state(UserState.access_denied)


@user_router.callback_query(UserState.access_denied)
async def user_registration(callback: CallbackQuery, state: FSMContext):
    info = await state.get_data()
    i, f, o = info['user_name'].split()
    try:
        db_connect = config.db.get_connect()
        cursor = db_connect.cursor()

        create_table_query = '''
            insert into users_data
            (id_tg, name, sec_name, last_name, phone_number, email, date_registration, sum_donation, status, level)
            values ( %s, %s, %s, %s, %s, %s, '03-09-2023', 0, true, 0);
     '''

        task_data = (
            info['user_id'],
            f,
            i,
            o,
            info['user_phone'],
            info['user_email']
        )

        cursor.execute(create_table_query, task_data)
        db_connect.commit()
        cursor.close()
        db_connect.close()
        
    except:
        pass

    await bot.send_message(callback.from_user.id, "Спасибо за регистрацию!", reply_markup=donation_keyboard)
    await state.set_state(UserState.auntificatet)


@user_router.message(F.text == 'Пожертвовать' and UserState.auntificatet)
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
async def checkout_process(pre_checkout_query: PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    await state.set_state(PurchaseState.waiting_reply)


@user_router.message(PurchaseState.waiting_reply)
async def successful_payment(message: Message, state: FSMContext):
    await state.clear()
    db_connect = config.db.get_connect()
    cursor = db_connect.cursor()
    cursor.execute(
        f"select * from update_by_user_id({message.from_user.id}, {message.successful_payment.total_amount // 100});")
    db_connect.commit()
    cursor.close()
    
    text = str(pd.read_sql(
        f"select * from get_discounts_by_user_id({message.from_user.id});", db_connect))

    await message.answer(text=text)
    await message.answer(f'Спасибо за покупку! {message.successful_payment.total_amount // 100} {message.successful_payment.currency}')
    db_connect.close()