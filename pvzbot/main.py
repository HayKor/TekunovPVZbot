import asyncio
import logging

from aiogram import Bot, Dispatcher
from callback import router as callback_router
from commands import router as commands_router
from config import config
from database.database import create_all
from database.engine import engine
from handlers import router as handlers_router
from scheduler import scheduler, set_scheduled_jobs


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s   %(name)-25s %(levelname)-8s %(message)s",
    )

    bot = Bot(
        token=config.bot_token,
    )
    dp = Dispatcher()
    dp.include_router(commands_router)
    dp.include_router(callback_router)
    dp.include_router(handlers_router)

    set_scheduled_jobs(bot=bot)

    try:
        scheduler.start()
        await create_all(engine=engine)

        # THIS GOES LAST
        await dp.start_polling(bot)

    finally:
        await bot.session.close()
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
