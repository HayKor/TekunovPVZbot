import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message()
async def send_pvz_poll(message: types.Message):
    await message.reply(
        text=message.text,
    )


async def main():
    logging.basicConfig(
        level=logging.INFO,
    )
    sched = AsyncIOScheduler()

    try:
        await dp.start_polling(bot)
        sched.start()
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
