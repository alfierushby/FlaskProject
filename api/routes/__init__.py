from flask import Blueprint, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from api.routes.actors import actors_router
from api.routes.films import films_router

routes = Blueprint('api',__name__, url_prefix='/api')

@routes.errorhandler(ValidationError)
def handle_validation_error(error):
    return error.messages, 400

@routes.errorhandler(IntegrityError)
def handle_integrity_error(error):
    return ("The integrity of the database cannot be met when trying this request. Usually this means you are trying "
            "to add a duplicate entity"), 400

@routes.errorhandler(500)
def handle_generic_error(error):
    return "Internal Server Error", 500

@routes.errorhandler(400)
def custom_error_400(msg):
    return msg, 400

@routes.errorhandler(ValueError)
def handle_value_error(error):
    if "list.remove(x)" in error.args[0]:
        return "Cannot remove the entity because it doesn't exist", 400
    else:
        return "ValueError occurred", 400

routes.register_blueprint(actors_router)
routes.register_blueprint(films_router)


