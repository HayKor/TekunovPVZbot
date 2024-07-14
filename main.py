import asyncio
import logging
from aiogram import Bot, Dispatcher, types

from apscheduler import AsyncScheduler
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message()
async def send_pvz_poll(message: types.Message):
    # await message.answer_poll(
    #     question="Your answer?",
    #     options=["A)", "B)", "C"],
    #     type="quiz",
    #     correct_option_id=1,
    #     is_anonymous=False,
    # )
    await message.reply(text=message.text)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
