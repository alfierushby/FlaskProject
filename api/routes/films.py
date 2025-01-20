from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import DBAPIError

from api.models import db
from api.models.actor import Actor
from api.models.film import Film
from api.schemas.film import film_schema, films_schema
from api.schemas.actor import actor_schema, actors_schema

# Create a "Blueprint" or module
# We can insert this into our flask app
films_router = Blueprint('films', __name__, url_prefix='/films')


@films_router.get('/')
def read_all_films():
    films = Film.query.all()
    return films_schema.dump(films)


@films_router.get('/<film_id>')
def read_film(film_id):
    film = Film.query.get_or_404(film_id)
    return film_schema.dump(film)


@films_router.post('/')
def create_film():
    film_data = request.json

    try:
        film_schema.load(film_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    film = Film(**film_data)
    db.session.add(film)
    db.session.commit()

    return film_schema.dump(film)


@films_router.delete('/<film_id>')
def delete_film(film_id):
    film = Film.query.get_or_404(film_id)

    try:
        db.session.delete(film)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.commit()

    return film_schema.dump(film)


@films_router.put('/<film_id>')
def update_actor(film_id):
    film = Film.query.get_or_404(film_id)

    title = request.json['title']
    description = request.json['description']
    release_year = request.json['release_year']
    length = request.json['length']

    film.title = title
    film.description = description
    film.release_year = release_year
    film.length = length

    db.session.commit()
    return film_schema.dump(film)


@films_router.get('/<film_id>/actors')
def get_actors(film_id):
    film = Film.query.get_or_404(film_id)
    actors = film.actors

    return actors_schema.dump(actors)


@films_router.post('<film_id>/actors/<actor_id>')
def add_actor(film_id, actor_id):
    film = Film.query.get_or_404(film_id)
    actor = Actor.query.get_or_404(actor_id)
    film.actors.append(actor)
    try:
        db.session.commit()
    except DBAPIError:
        return jsonify("You tried to add an actor that already exists."), 400
    return actor_schema.dump(actor)


@films_router.delete('<film_id>/actors/<actor_id>')
def delete_actor(film_id, actor_id):
    film = Film.query.get_or_404(film_id)
    actor = Actor.query.get_or_404(actor_id)
    film.actors.remove(actor)
    db.session.commit()
    return actor_schema.dump(actor)
