import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from Database.engine import create_db, drop_db
from Keyboards import reply
from Keyboards import inline
from states import InfoStates

from Routers.maps import map_router
from Routers.team import team_router
from Routers.info_type import info_router
from Routers.admin import admin_router
from Routers.place_description import place_router

ALLOWED_UPDATES = ['message', 'edited_messages', 'callback_query']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('BOT_TOKEN'))

dp = Dispatcher()
dp.include_routers(map_router, team_router, info_router, admin_router, place_router)


@dp.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет! Я бот, который подскажет основные фишки и полезные раскидки на картах в CS 2",
                         reply_markup=reply.del_kb)
    await message.answer("Выбери карту, о которой хочешь узнать информацию", reply_markup=inline.start_kb)
    await state.set_state(InfoStates.CHOOSE_MAP)


async def main():
    # await drop_db()
    await create_db()
    await bot.delete_webhook()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
