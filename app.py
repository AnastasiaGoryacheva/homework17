from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Int()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

api = Api(app)
api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}

movies_ns = api.namespace("movies")
directors_ns = api.namespace("directors")
genres_ns = api.namespace("genres")


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        if director_id and genre_id:
            movies = Movie.query.filter(Movie.director_id == director_id, Movie.genre_id == genre_id).all()
        elif director_id:
            movies = Movie.query.filter(Movie.director_id == director_id)
        elif genre_id:
            movies = Movie.query.filter(Movie.genre_id == genre_id)
        else:
            movies = Movie.query.all()
        return movies_schema.dump(movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        db.session.add(new_movie)
        db.session.commit()
        db.session.close()
        return "", 201


@movies_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id):
        movie = Movie.query.get(id)
        return movie_schema.dump(movie), 200

    def put(self, id):
        movie = Movie.query.get(id)
        req_json = request.json

        movie.id = req_json.get['id']
        movie.title = req_json.get['title']
        movie.description = req_json.get['description']
        movie.trailer = req_json.get['trailer']
        movie.year = req_json.get['year']
        movie.rating = req_json.get['rating']
        movie.genre_id = req_json.get['genre_id']
        movie.director_id = req_json.get['director_id']

        db.session.add(movie)
        db.session.commit()
        db.session.close()
        return "", 204

    def delete(self, id):
        movie = Movie.query.get(id)

        db.session.delete(movie)
        db.session.commit()
        db.session.close()
        return "", 204


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = Director.query.all()
        return directors_schema.dump(directors), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        db.session.add(new_director)
        db.session.commit()
        db.session.close()
        return "", 201


@directors_ns.route('/<int:id>')
class DirectorView(Resource):
    def get(self, id):
        director = Director.query.get(id)
        return director_schema.dump(director), 200

    def put(self, id):
        director = Director.query.get(id)
        req_json = request.json

        director.id = req_json.get['id']
        director.name = req_json.get['name']

        db.session.add(director)
        db.session.commit()
        db.session.close()
        return "", 204

    def delete(self, id):
        director = Director.query.get(id)

        db.session.delete(director)
        db.session.commit()
        db.session.close()
        return "", 204


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = Genre.query.all()
        return genres_schema.dump(genres), 200

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        db.session.add(new_genre)
        db.session.commit()
        db.session.close()
        return "", 201


@genres_ns.route('/<int:id>')
class GenreView(Resource):
    def get(self, id):
        genre = Genre.query.get(id)
        return genre_schema.dump(genre), 200

    def put(self, id):
        genre = Genre.query.get(id)
        req_json = request.json

        genre.id = req_json.get['id']
        genre.name = req_json.get['name']

        db.session.add(genre)
        db.session.commit()
        db.session.close()
        return "", 204

    def delete(self, id):
        genre = Genre.query.get(id)

        db.session.delete(genre)
        db.session.commit()
        db.session.close()
        return "", 204

if __name__ == '__main__':
    app.run()
