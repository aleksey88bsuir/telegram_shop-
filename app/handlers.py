from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command


router = Router()


@router.message(CommandStart())
async def app_start(message: Message):
    await message.answer("Hello world!")
