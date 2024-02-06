import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.bot_config import load_config
from keyboards.keyboards import set_commands
from database.database import Database
from handlers import (registration, cmd_and_common, profile_edit,
                      cart, profile_orders, market)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    config = load_config()
    bot = Bot(token=config.bot_token)
    dp = Dispatcher()
    database = Database()
    database.start_db()

    dp.include_router(router=registration.router)
    dp.include_router(router=cmd_and_common.router)
    dp.include_router(router=profile_edit.router)
    dp.include_router(router=cart.router)
    # dp.include_router(router=profile_orders.router)
    dp.include_router(router=market.router)
    await bot.set_my_commands(set_commands())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())