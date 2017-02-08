from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///luoo.db')
DBSession = sessionmaker(bind=engine)
Base = declarative_base()

class magazine(Base):
    __tablename__ = 'magazine_info'
    id = Column(Integer, primary_key=True)
    magazine_id = Column(String(256))
    magazine_name = Column(String(256))
    magazine_tag = Column(String(256))

class music(Base):
    __tablename__ = 'music_info'
    id = Column(Integer, primary_key=True)
    music_name = Column(String(256))
    magazine_id = Column(String(256))
    music_artist = Column(String(256))
    music_save_path = Column(String(256))

class favorite(Base):
    __tablename__ = 'favorite'
    id = Column(Integer, primary_key=True)
    music_name = Column(String(256))
    magazine_id = Column(String(256))
    music_artist = Column(String(256))
    music_save_path = Column(String(256))