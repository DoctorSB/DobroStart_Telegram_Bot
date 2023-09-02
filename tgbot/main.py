import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from handlers import admin_router
from payments import payment_router

logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(storage=storage)





async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    # for router in [admin_router,...]:
    dp.include_router(admin_router)
    dp.include_router(payment_router)
    await dp.start_polling(bot)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот выключен!")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
