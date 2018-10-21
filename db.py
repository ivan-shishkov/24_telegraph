from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///telegraph.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    header = Column(String(150))
    signature = Column(String(50))
    body = Column(Text)
    published = Column(Date)
    path = Column(Text, index=True, unique=True)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
