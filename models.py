from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

model = declarative_base()


class Users(model):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    username = Column(String)
    is_admin = Column(Integer)


class Movies(model):
    __tablename__ = 'movies'

    id = Column(String, primary_key=True)
    name = Column(String)
    director = Column(String)
    popularity = Column(Float)
    imdb_score = Column(Float)
    genre = Column(String)
    is_active = Column(Integer, default=1)
