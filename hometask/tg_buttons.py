from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f"Привет")],
    [KeyboardButton(text=f"Пока")]
], resize_keyboard=True)

inline_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новости", url="https://dzen.ru/news")],
    [InlineKeyboardButton(text="Музыка", url="https://music.yandex.ru/")],
    [InlineKeyboardButton(text="Видео", url="https://www.youtube.com/")]
])

show_more = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
])

def dynamic_buttons():
    builder = InlineKeyboardBuilder()
    options = ["Опция 1", "Опция 2"]
    for option in options:
        builder.add(InlineKeyboardButton(text=option, callback_data=option))
    return builder.as_markup()
