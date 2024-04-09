from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from Database.models import Position, Place, Map


async def get_map_id(session: AsyncSession, name: str):
    map_name_lower = name.lower()
    query = select(Map).where(func.lower(Map.name) == map_name_lower)
    result = await session.execute(query)
    map_id = result.scalars().first().id
    return int(map_id)


async def orm_add_position(session: AsyncSession, data: dict):
    map_id = await get_map_id(session, data['CHOOSE_MAP'])
    add_data_position = Position(
        name=data['ADD_PLACE'],
        type=data['CHOOSE_INFO'],
        team=data['CHOOSE_TEAM'],
        map_id=map_id
    )
    session.add(add_data_position)
    await session.commit()


async def orm_get_position(session: AsyncSession, data: dict):
    map_id = await get_map_id(session, data['CHOOSE_MAP'])
    query = select(Position)\
        .where(Position.map_id == map_id)\
        .where(Position.team == data['CHOOSE_TEAM'])\
        .where(Position.type == data['CHOOSE_INFO'])
    result = await session.execute(query)
    positions = []
    for row in result.scalars().all():
        positions.append({'id': row.id, 'name': row.name})
    return positions


async def orm_add_place(session: AsyncSession, data: dict):
    add_data_place = Place(
        description=data['ADD_DESCRIPTION'],
        photo=data['ADD_PHOTO'],
        number=int(data['ADD_NUMBER']),
        position_id=int(data['POSITION_ID'])
    )
    session.add(add_data_place)
    await session.commit()


async def orm_get_place(session: AsyncSession, position_id: str):
    position_id = int(position_id)
    query = select(Place).where(Place.position_id == position_id)
    result = await session.execute(query)
    places = []
    for row in result.scalars().all():
        places.append({'number': row.number, 'photo': row.photo, 'description': row.description})
    return places
