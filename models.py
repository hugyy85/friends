from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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

# Base.metadata.create_all(engine)

def add_data_to_db(data: list) -> None:
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all(data)
    session.commit()
