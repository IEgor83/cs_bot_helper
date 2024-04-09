import os

from aiogram import F, types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from Keyboards import inline, reply
from Keyboards.maps_inline_keyboard import generate_inline_position_keyboard
from states import InfoStates, AddItemStates
from Database.engine import session_maker
from Database.models import Position, Place, Map, InfoType
from Database.orm_query import *

admin_router = Router()
admin_id = int(os.getenv('ADMIN_ID'))


states_messages = {
    AddItemStates.ADD_PHOTO: 'Фото позиции',
    AddItemStates.ADD_DESCRIPTION: 'Описание'
}

info_type = {
    InfoType.smoke: "Выбери куда и откуда ты хочешь кинуть смок",
    InfoType.flash: "Выбери куда и откуда ты хочешь кинуть флешку",
    InfoType.fire: "Выбери куда и откуда ты хочешь кинуть коктейль молотова / зажигательную гранату",
    InfoType.position: "Выбери позиции или подсадки"
}


@admin_router.message(InfoStates.CHOOSE_POSITION, Command("add"))
async def add_new_position(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await message.answer("Добавление новой информации")
        await state.set_state(AddItemStates.ADD_PLACE)
        await message.answer("Введите позицию (если это граната, то откуда и куда)")
    else:
        await message.answer("Я вас не понимаю, выберите позицию из списка")


@admin_router.message(InfoStates.POSITION_DESCRIPTION, Command("add"))
async def add_new_place(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await message.answer("Добавление информации о позиции")
        await state.update_data(PREVIOUS_STATE=InfoStates.POSITION_DESCRIPTION)
        await state.set_state(AddItemStates.ADD_PHOTO)
        await message.answer("Фото позиции")


@admin_router.message(AddItemStates.ADD_PLACE, (F.text != 'Назад') & (F.text != 'В начало'))
async def add_new_photo(message: types.Message, state: FSMContext, session: AsyncSession = session_maker()):
    if message.from_user.id == admin_id:
        await state.update_data(ADD_PLACE=message.text)
        data = await state.get_data()
        await orm_add_position(session, data)
        await message.answer(f"Добавлено: {message.text}")
    else:
        await message.answer("У вас нет прав, на это действие")


@admin_router.message(AddItemStates.ADD_PHOTO, F.photo)
async def add_new_description(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await state.update_data(ADD_PHOTO=message.photo[-1].file_id)
        await message.answer(f"Добавлено: {message.photo[-1].file_id}")
        await state.update_data(PREVIOUS_STATE=AddItemStates.ADD_PHOTO)
        await state.set_state(AddItemStates.ADD_DESCRIPTION)
        await message.answer("Описание")
    else:
        await message.answer("У вас нет прав, на это действие")


@admin_router.message(AddItemStates.ADD_DESCRIPTION, (F.text != 'Назад') & (F.text != 'В начало'))
async def add_new_number(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await message.answer(f"Добавлено: {message.text}")
        await state.update_data(ADD_DESCRIPTION=message.text)
        await state.update_data(PREVIOUS_STATE=AddItemStates.ADD_DESCRIPTION)
        await state.set_state(AddItemStates.ADD_NUMBER)
        await message.answer("Номер")
    else:
        await message.answer("У вас нет прав, на это действие")


@admin_router.message(AddItemStates.ADD_NUMBER, (F.text != 'Назад') & (F.text != 'В начало'))
async def save_place_info_db(message: types.Message, state: FSMContext, session: AsyncSession = session_maker()):
    if message.from_user.id == admin_id:
        await message.answer(f"Добавлено: {message.text}")
        await state.update_data(ADD_NUMBER=message.text)
        data = await state.get_data()
        await orm_add_place(session, data)
        await message.answer(f"Информация добавлена {str(data)}")
        await state.set_state(AddItemStates.ADD_PHOTO)
        await message.answer(f"прикрепите фото позиции или нажмите назад")
    else:
        await message.answer("У вас нет прав, на это действие")


@admin_router.message(StateFilter(AddItemStates.ADD_PLACE), (F.text == 'Назад') | (F.text == 'В начало'))
async def go_back_to_map_from_team(message: types.Message, state: FSMContext, session: AsyncSession = session_maker()):
    await state.set_state(InfoStates.CHOOSE_POSITION)
    data = await state.get_data()
    positions = await orm_get_position(session, data)
    await message.answer(info_type[data['CHOOSE_INFO']], reply_markup=generate_inline_position_keyboard(positions))


@admin_router.message(StateFilter(AddItemStates.ADD_PHOTO), (F.text == 'Назад') | (F.text == 'В начало'))
async def go_back_to_map_from_place(message: types.Message, state: FSMContext, session: AsyncSession = session_maker()):
    await state.set_state(InfoStates.CHOOSE_POSITION)
    data = await state.get_data()
    positions = await orm_get_position(session, data)
    await message.answer(info_type[data['CHOOSE_INFO']], reply_markup=generate_inline_position_keyboard(positions))


@admin_router.message(StateFilter(AddItemStates.ADD_DESCRIPTION, AddItemStates.ADD_NUMBER), F.text == 'Назад')
async def go_back_to_prev_stage(message: types.Message, state: FSMContext):
    data = await state.get_data()
    prev = data['PREVIOUS_STATE']
    await state.set_state(prev)
    await message.answer(states_messages[prev])
