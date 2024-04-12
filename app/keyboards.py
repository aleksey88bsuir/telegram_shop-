from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.data_base.requests import get_categories


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
