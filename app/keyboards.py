from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardRemove)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.data_base.requests import (get_categories, get_items_by_category,
                                    get_item_by_id)


main = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Каталог',
                                           callback_data='catalog')],
                     [InlineKeyboardButton(text='Корзина',
                                           callback_data='basket'),
                     InlineKeyboardButton(text='Контакты',
                                          callback_data='contacts')]])

to_main = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text='На главную', callback_data='to_main',)]])


async def show_all_categories():
    all_categories = await get_categories()
    main_keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        main_keyboard.add(InlineKeyboardButton(
            text=category.name,
            callback_data=f'category_{category.id}'))
    return main_keyboard.adjust(2).as_markup()


async def show_all_items_from_category(category_id: int):
    all_items = await get_items_by_category(category_id=category_id)
    items_keyboard = InlineKeyboardBuilder()
    for item in all_items:
        items_keyboard.add(InlineKeyboardButton(
            text=item.name,
            callback_data=f'item_{item.id}'))
    items_keyboard.add(InlineKeyboardButton(text='назад',
                                            callback_data='catalog'))
    return items_keyboard.adjust(1).as_markup()


async def show_item_by_id(item_id: int):
    item = await get_item_by_id(item_id=item_id)
    item_key = InlineKeyboardBuilder()
    item_key.add(InlineKeyboardButton(
            text=item.name,
            callback_data=f'item_{item.id}'))
    item_key.add(InlineKeyboardButton(text='назад', callback_data='to_main'))
    return item_key.adjust(1).as_markup()


def remove_keyboard():
    ReplyKeyboardRemove()
