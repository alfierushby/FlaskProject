from flask import Blueprint

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError

from api.routes.actors import actors_router
from api.routes.categories import categories_router
from api.routes.films import films_router


routes = Blueprint('api',__name__, url_prefix='/api')

@routes.errorhandler(ValidationError)
def handle_validation_error(error):
    return {
        "error": "Validation Error",
        "messages": error.messages,
        "error_type": "validation_error"
    }, 400

@routes.errorhandler(IntegrityError)
def handle_integrity_error(error):
    error_msg = str(error.orig)
    if 'duplicate entry' in error_msg.lower():
        return {
            "error": "Duplicate Entry",
            "message": "An entry with these details already exists",
            "error_type": "duplicate_error"
        }, 400
    else:
        return {
            "error": "Database Integrity Error",
            "message": "The request conflicts with database constraints",
            "error_type": "integrity_error"
        }, 400

@routes.errorhandler(500)
def handle_generic_error(error):
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "error_type": "internal_error"
    }, 500

@routes.errorhandler(400)
def custom_error_400(msg):
    return msg, 400

@routes.errorhandler(StaleDataError)
def handle_stale_data_error(error):
    return {
        "error": "Stale Data Error",
        "message": "Data does not exist",
        "error_type": "internal_error"
    }, 400

@routes.errorhandler(KeyError)
def handle_key_error(error):
    return {
        "error": "Key Error",
        "message": "Required key(s) do not exist in request",
        "error_type": "internal_error"
    }, 400

@routes.errorhandler(ValueError)
def handle_value_error(error):
    if "list.remove(x)" in error.args[0]:
        return {
            "error": "Removal Error",
            "message": "Cannot remove the entity because it doesn't exist in the list",
            "error_type": "removal_error"
        }, 400
    else:
        return {
            "error": "Invalid Value",
            "message": "One or more field values are invalid",
            "error_type": "value_error"
        }, 400

routes.register_blueprint(actors_router)
routes.register_blueprint(films_router)
routes.register_blueprint(categories_router)


