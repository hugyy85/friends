from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
import datetime

from config import START_DATE

import sys


engine = create_engine(r'sqlite:///vk.sqlite3', echo=False)

Base = declarative_base()


class User(Base):
    __tablename__ = 'vk_mobile'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    mobile = Column(Boolean)
    app = Column(String(50))
    datetime = Column(String(50))
    vk_id = Column(Integer)

    def __init__(self, first_name, last_name, mobile=True, app='991', datetime='today', vk_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.mobile = mobile
        self.app = app
        self.datetime = datetime
        self.vk_id = vk_id


def last_time_in_online(vk_name: str, limit=50) -> str:
    vk_id = _uid_to_id(vk_name)
    session = _make_session()
    query = session.query(User).filter_by(vk_id=vk_id).order_by(desc(User.id))[:limit]
    pretty_result = ''
    for info in query:
        pretty_result += '<p>mobile: {}, time: {} \n</p>'.format(info.mobile, info.datetime)
    return pretty_result


def how_long_in_online(limit=50, uid=None) -> str:
    session = _make_session()
    if uid:
        vk_id = _uid_to_id(uid)
        # select first_name, last_name, count(*) from vk_mobile where vk_id = vk_id
        query = session.query(User.first_name, User.last_name, func.count()).filter_by(vk_id=vk_id)
    else:
        # select first_name, last_name, count(*) from vk_mobile group by vk_id order by count(*);
        query = session.query(User.first_name, User.last_name, func.count()).group_by(User.vk_id).\
            order_by(func.count().desc())[:limit]

    pretty_result = ''
    delta_days = (datetime.datetime.now() - START_DATE).days
    for friend in query:
        minutes = friend[2]
        hours = round(minutes / 60, 1)
        pretty_result += '<p>{} {}: {} минут - {} часов - {} часов в день(c {}) </p>'.\
            format(friend[0], friend[1], minutes, hours, round(hours/delta_days, 1), START_DATE)

    return pretty_result


def _make_session():
    Session = sessionmaker(bind=engine)
    return Session()


def _uid_to_id(vk_uid):
    from connection import VkApiUse
    return VkApiUse().uid_to_id(vk_uid)


def add_data_to_db(data: list) -> None:
    session = _make_session()
    session.add_all(data)
    session.commit()


def create_db():
    Base.metadata.create_all(engine)
    print('Database has created')
    return True
