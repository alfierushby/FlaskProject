from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from api.models import db
from api.models.actor import Actor
from api.schemas.actor import actor_schema, actors_schema

# Create a "Blueprint" or module
# We can insert this into our flask app
actors_router = Blueprint('actors', __name__, url_prefix='/actors')


@actors_router.get('/')
def read_all_actors():
    actors = Actor.query.all()
    return actors_schema.dump(actors)


@actors_router.get('/<actor_id>')
def read_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor is None:
        return jsonify("Cannot find actor."), 404
    return actor_schema.dump(actor)


@actors_router.post('/')
def create_actor():
    actor_data = request.json

    try:
        actor_schema.load(actor_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    actor = Actor(**actor_data)
    db.session.add(actor)
    db.session.commit()

    return actor_schema.dump(actor)


@actors_router.delete('/<actor_id>')
def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor is None:
        return jsonify("Cannot find actor to delete."), 404

    try:
        db.session.delete(actor)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.commit()

    return actor_schema.dump(actor)


@actors_router.put('/<actor_id>')
def update_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor is None:
        return jsonify("Cannot find actor to edit."), 404

    first_name = request.json['first_name']
    last_name = request.json['last_name']

    actor.first_name = first_name
    actor.last_name = last_name

    db.session.commit()
    return actor_schema.dump(actor)
