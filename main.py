import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, FATHER_CHAT_ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# @dp.message()
# async def send_info(message: types.Message):
#     await bot.send_message(
#         chat_id=FATHER_CHAT_ID,
#         text=message.text,
#     )
#


async def send_to_father(bot: Bot):
    await bot.send_message(
        chat_id=FATHER_CHAT_ID,
        text="test every 5 sec",
    )


async def send_attendance_poll(bot: Bot):
    await bot.send_poll(
        chat_id=FATHER_CHAT_ID,
        question="What do you choose?",
        options=["A", "B", "C"],
        type="regular",
        is_anonymous=False,
    )


def set_scheduled_jobs(scheduler: AsyncIOScheduler, bot: Bot, *args, **kwargs):
    # scheduler.add_job(send_to_father, "interval", seconds=5, args=(bot,))
    scheduler.add_job(send_attendance_poll, "interval", seconds=5, args=(bot,))


async def main():
    logging.basicConfig(
        level=logging.INFO,
    )
    sched = AsyncIOScheduler()
    set_scheduled_jobs(scheduler=sched, bot=bot)

    try:
        sched.start()
        await dp.start_polling(bot)

    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
