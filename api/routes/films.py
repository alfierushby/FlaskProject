from flask import Blueprint, request
from sqlalchemy import or_
from api.models import db
from api.models.actor import Actor
from api.models.film import Film
from api.routes.common_functions import paginate_args, paginate_data
from api.schemas.film import film_schema, films_schema
from api.schemas.actor import actor_schema, actors_schema

# Create a "Blueprint" or module
# We can insert this into our flask app
films_router = Blueprint('films', __name__, url_prefix='/films')

@films_router.get('/')
def read_all_films():
    """
    :return: The films specified in the request args, or everything if no args are used
    """
    title = request.args.get('title','')
    description = request.args.get('description', '')
    page, per_page = paginate_args()

    films = Film.query.filter(or_(
        Film.title.contains(f"%{title}%")),
        Film.description.contains(f"%{description}")
                              ).paginate(page=page, per_page=per_page)
    return paginate_data(films_schema, films)

@films_router.get('/<film_id>')
def read_film(film_id):
    """
    :param film_id: id of the film in the database
    :return: The film specified by the ID, or a 404 if the film doesn't exist
    """
    film = Film.query.get_or_404(film_id)
    return film_schema.dump(film)

@films_router.post('/')
def create_film():
    """
    :return: The film object if it is successfully added, otherwise an error message
    """
    film_data = request.json

    film_schema.load(film_data)

    film = Film(**film_data)
    db.session.add(film)
    db.session.commit()

    return film_schema.dump(film),201


@films_router.delete('/<film_id>')
def delete_film(film_id):
    """
    :param film_id: The id of the film in the database
    :return: The film object that has been deleted, or an error message
    """
    film = Film.query.get_or_404(film_id)
    db.session.delete(film)
    db.session.commit()

    return film_schema.dump(film),200


@films_router.put('/<film_id>')
def update_film(film_id):
    """
    :param film_id: The id of the film in the database
    :return: The newly updated film object, or an error message
    """
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

    return film_schema.dump(film),200


@films_router.get('/<film_id>/actors')
def get_actors(film_id):
    """
    :param film_id:  The id of the film in the database
    :return: A list of actors that star in the film, or an error message
    """
    film = Film.query.get_or_404(film_id)
    actors = film.actors

    return actors_schema.dump(actors)


@films_router.post('/<film_id>/actors/<actor_id>')
def add_actor(film_id, actor_id):
    """
    :param film_id: The id of the film in the database
    :param actor_id: The id of the actor to star in the film
    :return: The actor object that has been added to the film, or an error message
    """
    film = Film.query.get_or_404(film_id)
    actor = Actor.query.get_or_404(actor_id)
    film.actors.append(actor)
    db.session.commit()
    return actor_schema.dump(actor),201


@films_router.delete('/<film_id>/actors/<actor_id>')
def delete_actor(film_id, actor_id):
    """
    :param film_id: The id of the film in the database
    :param actor_id: The id of the actor to be removed from the film
    :return: The actor removed from the film, or an error message
    """
    film = Film.query.get_or_404(film_id)
    actor = Actor.query.get_or_404(actor_id)
    film.actors.remove(actor)

    db.session.commit()
    return actor_schema.dump(actor),200
