from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Назад"),
            KeyboardButton(text="В начало")
        ]
    ],
    resize_keyboard=True,
)

del_kb = ReplyKeyboardRemove()
