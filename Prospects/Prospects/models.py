
from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary

from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()

def db_connect():

    """ Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance. """

    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class MetaDataDB(DeclarativeBase):
    __tablename__ = 'meta_data'

    
    ep_id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    date_of_birth = Column(DateTime)
    hometown = Column(String(100))
    country = Column(String(100))
    youth_team = Column(String(100))
    position = Column(String(20))
    height = Column(Float)
    weight = Column(Integer)
    shoots = Column(String(10))

class PlayerStatsDB(DeclarativeBase):
    __tablename__ = 'player_stats'

    ep_id = Column(Integer, primary_key=True)
    season = Column(String(20))
    team = Column(String(100))
    league = Column(String(20))
    games_played = Column(Integer)
    goals = Column(Integer)
    assists = Column(Integer)
    penalty_min = Column(Integer)
    plus_minus = Column(Integer)
