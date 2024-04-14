from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboards as kw
from app.data_base.requests import get_item_by_id


router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == "to_main")
async def app_start(message: Message | CallbackQuery):
    if isinstance(message, Message):
        await message.answer("Добро пожаловать в интернет-магазин!",
                             reply_markup=kw.main)
    else:
        await message.message.edit_text("Добро пожаловать в интернет-магазин!",
                                        reply_markup=kw.main)


@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.message.edit_text(
        'Выберите категорию',
        reply_markup=await kw.show_all_categories())


@router.callback_query(F.data.startswith('category_'))
async def catalog(callback: CallbackQuery):
    await callback.message.edit_text(
        'Выберите товар',
        reply_markup=await kw.show_all_items_from_category(
            int(callback.data.split('_')[1])))


@router.callback_query(F.data.startswith('item_'))
async def catalog(callback: CallbackQuery):
    item_id = int(callback.data.split('_')[1])
    item = await get_item_by_id(item_id)
    await callback.message.answer(f'{item.name}\n'
                                  f'{item.description}\n'
                                  f'{item.price/100} BYN',
                                  reply_markup=kw.to_main)


#
# @router.message(F.text == "Корзина")
# async def basket(message: Message):
#     await message.answer('')
#
#
# @router.message(F.text == "Контакты")
# async def contacts(message: Message):
#     await message.answer('')
