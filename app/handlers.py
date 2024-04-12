from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboards as kw

router = Router()


@router.message(CommandStart())
async def app_start(message: Message):
    await message.answer("Добро пожаловать в интернет-магазин!",
                         reply_markup=kw.main)


@router.message(F.text == "Каталог")
async def catalog(message: Message):
    await message.answer('Выберите категорию',
                         reply_markup=await kw.show_all_categories())


@router.callback_query(F.data.startswith('category_'))
async def catalog(callback: CallbackQuery):
    await callback.message.answer('Выберите товар')
    await callback.message.edit_text(
        'Выберите товар',
        reply_markup=await kw.show_all_items_from_category(
            int(callback.data.split('_')[1])))


#
# @router.message(F.text == "Корзина")
# async def basket(message: Message):
#     await message.answer('')
#
#
# @router.message(F.text == "Контакты")
# async def contacts(message: Message):
#     await message.answer('')
