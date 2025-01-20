from flask import Blueprint, abort, request


from api.models import db
from api.models.actor import Actor
from api.models.film import Film
from api.schemas.actor import actor_schema, actors_schema
from api.schemas.film import film_schema, films_schema

# Create a "Blueprint" or module
actors_router = Blueprint('actors', __name__, url_prefix='/actors')

@actors_router.get('/')
def read_all_actors():
    """
    :return: All the actors in the database
    """
    actors = Actor.query.all()
    return actors_schema.dump(actors)


@actors_router.get('/<actor_id>')
def read_actor(actor_id):
    """
    :param actor_id: id of the actor in the database
    :return: The actor specified by the ID, or a 404 if the actor doesn't exist
    """
    actor = Actor.query.get_or_404(actor_id)
    return actor_schema.dump(actor)


@actors_router.post('/')
def create_actor():
    """
    :return: The actor object if it is successfully added, otherwise an error message
    """
    actor_data = request.json

    actor_schema.load(actor_data)

    actor = Actor(**actor_data)
    db.session.add(actor)
    db.session.commit()

    return actor_schema.dump(actor),201


@actors_router.delete('/<actor_id>')
def delete_actor(actor_id):
    """
    :param actor_id: The id of the actor in the database
    :return: The actor object that has been deleted, or an error message
    """
    actor = Actor.query.get_or_404(actor_id)
    db.session.delete(actor)
    db.session.commit()

    return actor_schema.dump(actor),200


@actors_router.put('/<actor_id>')
def update_actor(actor_id):
    """
    :param actor_id: The id of the actor in the database
    :return: The newly updated actor object, or an error message
    """
    actor = Actor.query.get_or_404(actor_id)
    first_name = request.json['first_name']
    last_name = request.json['last_name']

    actor.first_name = first_name
    actor.last_name = last_name

    db.session.commit()

    return actor_schema.dump(actor),200


@actors_router.get('/<actor_id>/films')
def get_films(actor_id):
    """
    :param actor_id: The id of the actor in the database
    :return: A list of films that the actor stars in, or an error message
    """
    actor = Actor.query.get_or_404(actor_id)
    films = actor.films

    return films_schema.dump(films)


@actors_router.post('/<actor_id>/films/<film_id>')
def add_film(actor_id, film_id):
    """
    :param actor_id: The id of the actor in the database
    :param film_id: The id of the film the actor will star in
    :return: The film object that has been added to the actor's filmography, or an error message
    """
    actor = Actor.query.get_or_404(actor_id)
    film = Film.query.get_or_404(film_id)
    actor.films.append(film)
    db.session.commit()
    return film_schema.dump(film),201


@actors_router.delete('/<actor_id>/films/<film_id>')
def delete_film(actor_id, film_id):
    """
    :param actor_id: The id of the actor in the database
    :param film_id: The id of the film to be removed from the actor's filmography
    :return: The film removed from the actor's filmography, or an error message
    """
    actor = Actor.query.get_or_404(actor_id)
    film = Film.query.get_or_404(film_id)
    actor.films.remove(film)

    db.session.commit()
    return film_schema.dump(film),200
