from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

from Database.engine import session_maker
from Keyboards import inline
from Keyboards.maps_inline_keyboard import generate_inline_position_keyboard
from states import InfoStates
from Database.models import InfoType
from Database.orm_query import *


info_router = Router()


@info_router.callback_query(InfoStates.CHOOSE_INFO, F.data == 'smoke')
async def select_smokes(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession = session_maker()):
    await callback.message.answer("Выбраны смоки")
    await state.update_data(CHOOSE_INFO=InfoType.smoke)
    await state.set_state(InfoStates.CHOOSE_POSITION)
    data = await state.get_data()
    positions = await orm_get_position(session, data)
    await callback.answer()
    await callback.message.answer("Выбери куда и откуда ты хочешь кинуть смок",
                                  reply_markup=generate_inline_position_keyboard(positions))


@info_router.callback_query(InfoStates.CHOOSE_INFO, F.data == 'flash')
async def select_flashes(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession = session_maker()):
    await callback.message.answer("Выбраны флешки")
    await state.update_data(CHOOSE_INFO=InfoType.flash)
    await state.set_state(InfoStates.CHOOSE_POSITION)
    data = await state.get_data()
    positions = await orm_get_position(session, data)
    await callback.answer()
    await callback.message.answer("Выбери куда и откуда ты хочешь кинуть флешку",
                                  reply_markup=generate_inline_position_keyboard(positions))


@info_router.callback_query(InfoStates.CHOOSE_INFO, F.data == 'molotov')
async def select_molotov(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession = session_maker()):
    await callback.message.answer("Выбран Молотов")
    await state.update_data(CHOOSE_INFO=InfoType.fire)
    await state.set_state(InfoStates.CHOOSE_POSITION)
    data = await state.get_data()
    positions = await orm_get_position(session, data)
    await callback.answer()
    await callback.message.answer("Выбери куда и откуда ты хочешь кинуть коктейль молотова",
                                  reply_markup=generate_inline_position_keyboard(positions))


@info_router.callback_query(InfoStates.CHOOSE_INFO, F.data == 'fire')
async def select_fire(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession = session_maker()):
    await callback.message.answer("Выбраны зажигательные гранаты")
    await state.update_data(CHOOSE_INFO=InfoType.fire)
    await state.set_state(InfoStates.CHOOSE_POSITION)
    data = await state.get_data()
    positions = await orm_get_position(session, data)
    await callback.answer()
    await callback.message.answer("Выбери куда и откуда ты хочешь кинуть зажигательную гранату",
                                  reply_markup=generate_inline_position_keyboard(positions))


@info_router.callback_query(InfoStates.CHOOSE_INFO, F.data == 'position')
async def select_positions(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession = session_maker()):
    await callback.message.answer("Выбраны позиции/подсадки")
    await state.update_data(CHOOSE_INFO=InfoType.position)
    await state.set_state(InfoStates.CHOOSE_POSITION)
    data = await state.get_data()
    positions = await orm_get_position(session, data)
    await callback.answer()
    await callback.message.answer("Выбери позиции или подсадки",
                                  reply_markup=generate_inline_position_keyboard(positions))


@info_router.message(InfoStates.CHOOSE_INFO, F.text == 'Назад')
async def go_back_to_map_from_info(message: types.Message, state: FSMContext):
    await state.update_data(CHOOSE_TEAM=None)
    await state.set_state(InfoStates.CHOOSE_TEAM)
    await message.answer("Выбери сторону, за которую играешь", reply_markup=inline.team_kb)


@info_router.message(InfoStates.CHOOSE_INFO, F.text == 'В начало')
async def go_back_to_start_from_info(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(InfoStates.CHOOSE_MAP)
    await message.answer("Выбери карту, о которой хочешь узнать информацию", reply_markup=inline.start_kb)


@info_router.message(InfoStates.CHOOSE_INFO, F.text)
async def select_none_info(message: types.Message):
    await message.answer("Извините, я вас не понимаю, попробуйте выбрать параметр из списка")
