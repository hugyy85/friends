from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, func, distinct
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc

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


def show_info_about_id(vk_id: int, limit=50) -> str:
    session = _make_session()
    query = session.query(User).filter_by(vk_id=vk_id).order_by(desc(User.id))[:limit]
    pretty_result = ''
    for info in query:
        pretty_result += '<p>mobile: {}, time: {} \n</p>'.format(info.mobile, info.datetime)
        # print(info.first_name, info.last_name, info.mobile, info.datetime)
    return pretty_result


def show_how_long_in_online(limit=50) -> str:
    # select *, count(*) from vk_mobile group by vk_id order by count(*);
    session = _make_session()
    query = session.query(User.first_name, User.last_name, func.count()).group_by(User.vk_id).\
        order_by(func.count(distinct(User.vk_id)))[:limit]
    pretty_result = ''
    for friend in query:
        pretty_result += '<p>{} {}: {} min </p>'.format(friend[0], friend[1], friend[2])

    return pretty_result


def _make_session():
    Session = sessionmaker(bind=engine)
    return Session()


def add_data_to_db(data: list) -> None:
    session = _make_session()
    session.add_all(data)
    session.commit()


if __name__ == '__main__':
    # Base.metadata.create_all(engine)

    if len(sys.argv) > 1:
        for param in sys.argv[1:]:
            show_info_about_id(param)
