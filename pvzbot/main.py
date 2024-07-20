import asyncio
import logging

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from commands import router as commands_router
from config import config
from database.database import create_all
from database.engine import engine
from scheduler import set_scheduled_jobs


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
    )

    bot = Bot(
        token=config.bot_token,
    )
    dp = Dispatcher()
    dp.include_router(commands_router)

    sched = AsyncIOScheduler()
    set_scheduled_jobs(bot=bot)

    try:
        sched.start()
        await create_all(engine=engine)

        # THIS GOES LAST
        await dp.start_polling(bot)

    finally:
        await bot.session.close()
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
