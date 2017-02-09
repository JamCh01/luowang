from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
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
    magazine_total = Column(String(256))
    new = Column(Integer, default=1)


class music(Base):
    __tablename__ = 'music_info'
    id = Column(Integer, primary_key=True)
    music_name = Column(String(256))
    magazine_id = Column(String(256))
    music_artist = Column(String(256))
    music_save_path = Column(String(256))
    play_time = Column(Integer)



class favorite(Base):
    __tablename__ = 'favorite'
    id = Column(Integer, primary_key=True)
    music_name = Column(String(256))
    magazine_id = Column(String(256))
    music_artist = Column(String(256))
    music_save_path = Column(String(256))
    count = Column(Integer, default=1)
    play_time = Column(Integer)
    add_time = Column(TIMESTAMP, default=func.current_timestamp())


class check(object):

    def __init__(self):
        pass

    def check_magazine(self, magazine_id):
        # 检验期刊是否存在数据库中
        check_session = DBSession()
        try:
            check_session.query(magazine).filter_by(
                magazine_id=magazine_id).one()
            return True
        except Exception as e:
            return False
        finally:
            check_session.close()

    def check_music(self, magazine_id, music_name):
        # 检验音乐是否存在数据库中
        check_session = DBSession()
        try:
            check_session.query(music).filter_by(
                magazine_id=magazine_id, music_name=music_name).one()
            return True
        except Exception as e:
            return False
        finally:
            check_session.close()

    def check_favorite(self, magazine_id, music_name):
        # 检验音乐是否存在数据库中
        check_session = DBSession()
        try:
            check_session.query(favorite).filter_by(
                magazine_id=magazine_id, music_name=music_name).one()
            return True
        except Exception as e:
            return False
        finally:
            check_session.close()

    def check_new(self, magazine_id):
        # 检验期刊是否为新期刊
        check_session = DBSession()
        try:
            new = check_session.query(magazine.new).filter_by(magazine_id=magazine_id).one()[0]
            if new == 1:
                return True
            else:
                return False
        except Exception as e:
            return False
        finally:
            check_session.close()