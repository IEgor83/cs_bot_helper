from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Mirage", callback_data="mirage"),
            InlineKeyboardButton(text="Inferno", callback_data="inferno")
        ],
        [
            InlineKeyboardButton(text="Dust 2", callback_data="dust2"),
            InlineKeyboardButton(text="Nuke", callback_data="nuke")
        ],
        [
            InlineKeyboardButton(text="Vertigo", callback_data="vertigo"),
            InlineKeyboardButton(text="Ancient", callback_data="ancient")
        ],
        [
            InlineKeyboardButton(text="Overpass", callback_data="overpass"),
            InlineKeyboardButton(text="Anubis", callback_data="anubis")
        ]
    ]
)


team_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="terrorists", callback_data="t"),
            InlineKeyboardButton(text="counter-terrorists", callback_data="ct")
        ]
    ]
)


options_t_kb = InlineKeyboardBuilder()
options_t_kb.add(
    InlineKeyboardButton(text="Смоки", callback_data="smoke"),
    InlineKeyboardButton(text="Флешки", callback_data="flash"),
    InlineKeyboardButton(text="Молотов", callback_data="molotov"),
    InlineKeyboardButton(text="Подсадки/Позиции", callback_data="position"),
)
options_t_kb.adjust(1, 1, 1, 1)

options_ct_kb = InlineKeyboardBuilder()
options_ct_kb.add(
    InlineKeyboardButton(text="Смоки", callback_data="smoke"),
    InlineKeyboardButton(text="Флешки", callback_data="flash"),
    InlineKeyboardButton(text="Зажигательная граната", callback_data="fire"),
    InlineKeyboardButton(text="Подсадки/Позиции", callback_data="position"),
)
options_ct_kb.adjust(1, 1, 1, 1)
