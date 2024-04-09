from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_inline_position_keyboard(positions):
    keyboard = [[InlineKeyboardButton(text='')] for _ in range(len(positions))]
    for i, position in enumerate(positions):
        keyboard[i][0] = InlineKeyboardButton(text=position['name'], callback_data=str(position['id']))
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
