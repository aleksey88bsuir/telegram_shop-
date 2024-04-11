import asyncio

from aiogram import Bot, Dispatcher
from app.config import TOKEN
from app.data_base.models import async_main


async def main():
    await async_main()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
