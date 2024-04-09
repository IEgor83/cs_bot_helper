import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Map(Base):
    __tablename__ = 'maps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    position = relationship("Position", back_populates="map")


class InfoType(enum.Enum):
    smoke = 'smoke'
    flash = 'flash'
    fire = 'fire'
    position = 'position'


class Team(enum.Enum):
    ct = 'ct'
    t = 't'


class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    type = Column(Enum(InfoType), name='information_type')
    team = Column(Enum(Team), name='team')
    map_id = Column(Integer, ForeignKey('maps.id'))

    map = relationship("Map", back_populates="position")
    place = relationship("Place", back_populates="map_position")


class Place(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer)
    position_id = Column(Integer, ForeignKey('positions.id'))
    photo = Column(String)
    description = Column(Text)

    map_position = relationship("Position", back_populates="place")
