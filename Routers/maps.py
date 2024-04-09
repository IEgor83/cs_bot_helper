from aiogram import F, types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from Keyboards import inline, reply
from states import InfoStates


map_router = Router()
maps = [
    'mirage',
    'inferno',
    'dust2',
    'nuke',
    'vertigo',
    'ancient',
    'overpass',
    'anubis'
]


def is_map_selected(callback_query: types.CallbackQuery):
    return callback_query.data in maps


@map_router.callback_query(InfoStates.CHOOSE_MAP, is_map_selected)
async def select_map(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"Выбрана карта {callback.data.capitalize()}", reply_markup=reply.start_kb)
    await state.update_data(CHOOSE_MAP=callback.data)
    await state.set_state(InfoStates.CHOOSE_TEAM)
    await callback.answer()
    await callback.message.answer("Выбери сторону, за которую играешь", reply_markup=inline.team_kb)


@map_router.message(InfoStates.CHOOSE_MAP, (F.text == 'Назад') | (F.text == 'В начало'))
async def go_back_to_start_from_map(message: types.Message):
    await message.answer("Вы находитесь в самом начале")
    await message.answer("Выбери карту, о которой хочешь узнать информацию", reply_markup=inline.start_kb)


@map_router.message(InfoStates.CHOOSE_MAP, F.text)
async def select_none_map(message: types.Message):
    await message.answer("Такой карты я не знаю")
