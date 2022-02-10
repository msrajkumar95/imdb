import json
import os
import uuid
from sqlalchemy import create_engine, orm
from models import model, Movies, Users


db_path = os.path.join(os.path.dirname(__file__), "db.sqlite")
db_uri = 'sqlite:///{}'.format(db_path)

db = create_engine(db_uri, connect_args={'check_same_thread': False}, echo=False)
model.metadata.create_all(db)
session = orm.sessionmaker(db)()

row_to_dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}


def insert_record(data_dict):

    movie = Movies()
    movie.id = str(uuid.uuid4())
    movie.name = data_dict["name"]
    movie.director = data_dict["director"]
    movie.popularity = data_dict["99popularity"]
    movie.imdb_score = data_dict["imdb_score"]
    movie.genre = json.dumps(data_dict["genre"])

    session.add(movie)
    session.commit()


def insert_file_data():
    with open('movies_data.json') as f:
        for item in json.load(f):
            insert_record(item)


def insert_users():
    user1 = Users(id=str(uuid.uuid4()), username="admin", is_admin=True)
    session.add(user1)
    user2 = Users(id=str(uuid.uuid4()), username="rajkumar", is_admin=True)
    session.add(user2)
    session.commit()


if __name__ == '__main__':
    insert_users()
    insert_file_data()
