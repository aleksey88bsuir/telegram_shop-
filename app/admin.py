from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kw
from app.data_base.requests import get_users, set_item


admin = Router()


class NewsLetter(StatesGroup):
    message = State()
    confirm = State()


class AddItem(StatesGroup):
    name = State()
    description = State()
    price = State()
    photo = State()
    category = State()


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


@admin.message(AdminProtect(), Command('add_item'))
async def add_item(message: Message, state: FSMContext):
    await state.set_state(AddItem.name)
    await message.answer('Выберите название товара')


@admin.message(AdminProtect(), AddItem.name)
async def add_item_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddItem.category)
    await message.answer('Выберите категорию товара',
                         reply_markup=await kw.show_all_categories())


@admin.callback_query(AdminProtect(), AddItem.category)
async def add_item_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data.split('_')[1])
    await state.set_state(AddItem.price)
    await callback.answer('Категория успешно выбрана')
    await callback.message.answer('Введите цену товара')


@admin.message(AdminProtect(), AddItem.price)
async def add_item_price(message: Message, state: FSMContext):
    await state.update_data(price=int(message.text)*100)
    await state.set_state(AddItem.photo)
    await message.answer('Выберите путь к фотографии товара')


@admin.message(AdminProtect(), AddItem.photo, F.photo)
async def add_item_price(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(AddItem.description)
    await message.answer('Выберите описание товара')


@admin.message(AdminProtect(), AddItem.description)
async def add_item_price(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    data['is_active'] = 1
    await set_item(data)
    await message.answer('Товар успешно добавлен')
    await state.clear()

