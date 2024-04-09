from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

from Keyboards import inline
from states import InfoStates
from Database.models import Team

team_router = Router()


@team_router.callback_query(InfoStates.CHOOSE_TEAM, F.data == 't')
async def select_t(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выбраны террористы")
    await state.update_data(CHOOSE_TEAM=Team.t)
    await state.set_state(InfoStates.CHOOSE_INFO)
    await callback.answer()
    await callback.message.answer("Теперь выбери, что ты хочешь узнать", reply_markup=inline.options_t_kb.as_markup())


@team_router.callback_query(InfoStates.CHOOSE_TEAM, F.data == 'ct')
async def select_ct(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выбраны контр-террористы")
    await state.update_data(CHOOSE_TEAM=Team.ct)
    await state.set_state(InfoStates.CHOOSE_INFO)
    await callback.answer()
    await callback.message.answer("Теперь выбери, что ты хочешь узнать", reply_markup=inline.options_ct_kb.as_markup())


@team_router.message(InfoStates.CHOOSE_TEAM, (F.text == 'Назад') | (F.text == 'В начало'))
async def go_back_to_map_from_team(message: types.Message, state: FSMContext):
    await state.update_data(CHOOSE_MAP=None)
    await state.set_state(InfoStates.CHOOSE_MAP)
    await message.answer("Выбери карту, о которой хочешь узнать информацию", reply_markup=inline.start_kb)


@team_router.message(InfoStates.CHOOSE_TEAM, F.text)
async def select_none_team(message: types.Message):
    await message.answer("Такой команды я не знаю, выберите из предложенных вариантов")
