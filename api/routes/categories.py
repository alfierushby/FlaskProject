from flask import Blueprint, request
from sqlalchemy import or_

from api.models import db
from api.models.actor import Actor
from api.models.category import Category
from api.models.film import Film
from api.routes.common_functions import paginate_args, paginate_data, filter_data
from api.schemas.actor import actor_schema, actors_schema
from api.schemas.category import category_schema, categories_schema
from api.schemas.film import film_schema, films_schema

# Create a "Blueprint" or module
categories_router = Blueprint('categories', __name__, url_prefix='/categories')

@categories_router.get('/')
def read_all_categories():
    """
    :return: The categories specified in the request args, or everything if no args are used, all paginated
    """
    name = request.args.get('name','')
    page, per_page = paginate_args()

    categories = (filter_data(Category.query,Category,[('name',name)]).paginate(page=page, per_page=per_page))

    return paginate_data(categories_schema,categories)