from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

from Database.engine import session_maker
from Keyboards import inline
from Keyboards.maps_inline_keyboard import generate_inline_position_keyboard
from states import InfoStates
from Database.models import InfoType, Team
from Database.orm_query import *


place_router = Router()

info_type = {
    InfoType.smoke: "Выбери куда и откуда ты хочешь кинуть смок",
    InfoType.flash: "Выбери куда и откуда ты хочешь кинуть флешку",
    InfoType.fire: "Выбери куда и откуда ты хочешь кинуть коктейль молотова / зажигательную гранату",
    InfoType.position: "Выбери позиции или подсадки"
}


@place_router.callback_query(InfoStates.CHOOSE_POSITION, F.data)
async def get_place_data(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession = session_maker()):
    await state.set_state(InfoStates.POSITION_DESCRIPTION)
    await callback.message.answer("Результат")
    await state.update_data(POSITION_ID=callback.data)
    places = await orm_get_place(session, callback.data)
    places.sort(key=lambda x: x['number'])
    for place in places:
        await callback.message.answer_photo(photo=place['photo'], caption=place['description'])
    await callback.answer()


@place_router.message(InfoStates.POSITION_DESCRIPTION, F.text == 'Назад')
async def go_back_to_positions_from_place(message: types.Message, state: FSMContext,  session: AsyncSession = session_maker()):
    await state.set_state(InfoStates.CHOOSE_POSITION)
    data = await state.get_data()
    positions = await orm_get_position(session, data)
    await message.answer(info_type[data['CHOOSE_INFO']], reply_markup=generate_inline_position_keyboard(positions))


@place_router.message(InfoStates.CHOOSE_POSITION, F.text == 'Назад')
async def go_back_to_info_from_positions(message: types.Message, state: FSMContext):
    await state.set_state(InfoStates.CHOOSE_INFO)
    data = await state.get_data()
    if data['CHOOSE_TEAM'] == Team.ct:
        await message.answer("Теперь выбери, что ты хочешь узнать", reply_markup=inline.options_ct_kb.as_markup())
    else:
        await message.answer("Теперь выбери, что ты хочешь узнать", reply_markup=inline.options_t_kb.as_markup())


@place_router.message(InfoStates.POSITION_DESCRIPTION, F.text == 'В начало')
async def go_back_to_start_from_place(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(InfoStates.CHOOSE_MAP)
    await message.answer("Выбери карту, о которой хочешь узнать информацию", reply_markup=inline.start_kb)


@place_router.message(InfoStates.CHOOSE_POSITION, F.text == 'В начало')
async def go_back_to_start_from_positions(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(InfoStates.CHOOSE_MAP)
    await message.answer("Выбери карту, о которой хочешь узнать информацию", reply_markup=inline.start_kb)


@place_router.message(InfoStates.CHOOSE_POSITION, F.text)
async def select_none_info_choose_position(message: types.Message):
    await message.answer("Извините, я вас не понимаю")


@place_router.message(InfoStates.POSITION_DESCRIPTION, F.text)
async def select_none_info_choose_position(message: types.Message):
    await message.answer("Извините, я вас не понимаю")
