from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboards as kw
from app.data_base.requests import get_item_by_id, set_user


router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == "to_main")
async def app_start(message: Message | CallbackQuery):
    if isinstance(message, Message):
        await set_user(message.from_user.id)
        await message.answer("Добро пожаловать в интернет-магазин!",
                             reply_markup=kw.main)
    else:
        await message.answer('Вы вернулись на главную')
        await message.message.answer("Добро пожаловать в интернет-магазин!",
                                        reply_markup=kw.main)


@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.message.edit_text(
        'Выберите категорию',
        reply_markup=await kw.show_all_categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: Message | CallbackQuery):
    await callback.message.answer(
        'Выберите товар',
        reply_markup=await kw.show_all_items_from_category(
            int(callback.data.split('_')[1])))


@router.callback_query(F.data.startswith('item_'))
async def items(callback: CallbackQuery):
    item_id = int(callback.data.split('_')[1])
    item = await get_item_by_id(item_id)
    await callback.message.answer_photo(
        photo=item.photo,
        caption=f'{item.name}\n {item.description}\n {item.price/100} BYN',
        reply_markup=await kw.show_order_form(item_id))
