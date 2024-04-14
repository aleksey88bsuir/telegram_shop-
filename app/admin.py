from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kw
from app.data_base.requests import get_users


admin = Router()


class NewsLetter(StatesGroup):
    message = State()
    confirm = State()


class AdminProtect(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [6064376244]


@admin.message(AdminProtect(), Command('admin_panel'))
async def admin_panel(message: Message):
    await message.answer(
        text='Возможные команды: /newsletter',

    )


@admin.message(AdminProtect(), Command('newsletter'))
async def message(message: Message, state: FSMContext):
    await state.set_state(NewsLetter.message)
    await message.answer(
        'Отправьте сообщение, которое вы хотите разослать всем пользователям')


@admin.message(AdminProtect(), NewsLetter.message)
async def news_letter_message(message: Message, state: FSMContext):
    await message.answer('Подождите... Идёт рассылка')
    for user in await get_users():
        try:
            await message.send_copy(chat_id=user.id_tg)
        except Exception:
            pass
    await message.answer('Рассылка успешно завершена')
    await state.clear()
