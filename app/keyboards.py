from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.data_base.requests import get_categories, get_items_by_category


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог')],
                                     [KeyboardButton(text='Корзина'),
                                      KeyboardButton(text='Контакты')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню')


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
                                            callback_data='to_main'))
    return items_keyboard.adjust(1).as_markup()
