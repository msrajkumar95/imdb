import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from database import session, row_to_dict, insert_record
from flask import Flask, jsonify
from flask_restplus import Api, Resource, reqparse
from models import Users, Movies


app = Flask(__name__)
api = Api(app)

get_movies = reqparse.RequestParser()
get_movies.add_argument('name', help='Specify characters of movie name for search (Optional)')

update_movies = api.parser()
update_movies.add_argument('username', help='Username to check access')
update_movies.add_argument('id', help='ID of the movie')
update_movies.add_argument('name', help='Name of the movie to update')
update_movies.add_argument('director', help='Director name of the movie to update')
update_movies.add_argument('99popularity', help='99popularity value of the movie to update')
update_movies.add_argument('imdb_score', help='IMDB score of the movie to update')
update_movies.add_argument('genre', help='Genre of the movie to update')

add_movies = api.parser()
add_movies.add_argument('username', help='Username to check access')
add_movies.add_argument('name', help='Name of the movie')
add_movies.add_argument('director', help='Director name of the movie')
add_movies.add_argument('99popularity', help='99popularity value of the movie')
add_movies.add_argument('imdb_score', help='IMDB score of the movie')
add_movies.add_argument('genre', help='Genre of the movie')

delete_movies = api.parser()
delete_movies.add_argument('username', help='Username to check access')
delete_movies.add_argument('id', help='ID of the movie to delete')


def is_user_authenticated(username):
    return session.query(Users).filter(Users.username.is_(username)).scalar()


@api.route('/movies')
class MoviesResource(Resource):

    @api.doc(parser=get_movies)
    def get(self):
        args = get_movies.parse_args()
        name = args['name']
        if name:
            movies = session.query(Movies).filter(Movies.is_active.is_(1)).filter(
                Movies.name.like("%{}%".format(name))).all()
        else:
            movies = session.query(Movies).filter(Movies.is_active.is_(1)).all()
        return jsonify([row_to_dict(movie) for movie in movies])

    @api.doc(parser=update_movies)
    def put(self):
        data = update_movies.parse_args()
        username = data.get('username')
        data_dict = {
            "id": data.get('id'),
            "name": data.get('name'),
            "director": data.get('director'),
            "popularity": data.get('99popularity'),
            "imdb_score": data.get('imdb_score'),
            "genre": data.get('genre')
        }

        if is_user_authenticated(username):
            session.bulk_update_mappings(Movies, [data_dict])
            session.commit()
            return jsonify({"status": "success", "message": "Data updated successfully"})
        else:
            return jsonify({"status": "failure", "message": "User not authenticated to perform this action"})

    @api.doc(parser=add_movies)
    def post(self):
        data = add_movies.parse_args()
        username = data.get('username')
        data_dict = {
            "name": data.get('name'),
            "director": data.get('director'),
            "99popularity": data.get('99popularity'),
            "imdb_score": data.get('imdb_score'),
            "genre": data.get('genre')
        }

        if is_user_authenticated(username):
            insert_record(data_dict)
            return jsonify({"status": "success", "message": "Data updated successfully"})
        else:
            return jsonify({"status": "failure", "message": "User not authenticated to perform this action"})

    @api.doc(parser=delete_movies)
    def delete(self):
        data = delete_movies.parse_args()
        movie_id = data.get('id')
        username = data.get('username')
        data_dict = {
            "id": movie_id,
            "is_active": 0
        }

        if data_dict and is_user_authenticated(username):
            session.bulk_update_mappings(Movies, [data_dict])
            session.commit()
            return jsonify({"status": "success", "message": "Data deleted successfully"})
        else:
            return jsonify({"status": "failure", "message": "User not authenticated to perform this action"})


if __name__ == '__main__':
    app.run(debug=False)
