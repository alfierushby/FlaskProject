from flask import Blueprint, request

from api.models import db
from api.models.category import Category
from api.models.film import Film
from api.routes.common_functions import paginate_args, paginate_data, filter_data
from api.schemas.category import category_schema, categories_schema
from api.schemas.film import film_schema, films_schema

# Create a "Blueprint" or module
categories_router = Blueprint('categories', __name__, url_prefix='/categories')


@categories_router.get('/')
def read_all_categories():
    """
    :return: The categories specified in the request args, or everything if no args are used, all paginated
    """
    name = request.args.get('name', '')
    page, per_page = paginate_args()

    categories = (filter_data(Category.query, Category, [('name', name)]).paginate(page=page, per_page=per_page))

    return paginate_data(categories_schema, categories)


@categories_router.get('/<category_id>')
def read_category(category_id):
    """
    :param category_id: id of the category in the database
    :return: The category specified by the ID, or a 404 if the actor doesn't exist
    """
    category = Category.query.get_or_404(category_id)
    return category_schema.dump(category)


@categories_router.delete('/<category_id>')
def delete_category(category_id):
    """
    :param category_id: The id of the category in the database
    :return: The category object that has been deleted, or an error message
    """
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()

    return category_schema.dump(category), 200


@categories_router.post('/')
def create_category():
    """
    :return: The category object if it is successfully added, otherwise an error message
    """
    category_data = request.json

    category_schema.load(category_data)

    category = Category(**category_data)
    db.session.add(category)
    db.session.commit()

    return category_schema.dump(category), 201


@categories_router.put('/<category_id>')
def update_category(category_id):
    """
    :param category_id: The id of the category in the database
    :return: The newly updated category object, or an error message
    """
    category = Category.query.get_or_404(category_id)
    name = request.json['name']

    category.name = name

    db.session.commit()

    return category_schema.dump(category),200


@categories_router.get('/<category_id>/films')
def read_films(category_id):
    """
    :param category_id: id of the category in the database
    :return: The films that are in the specified category, or a 404 if the category doesn't exist
    """
    category = Category.query.get_or_404(category_id)
    title = request.args.get('title', '')
    description = request.args.get('description', '')
    page, per_page = paginate_args()

    films = (filter_data(category.films, Film, [('title', title), ('description', description)])
             .paginate(page=page, per_page=per_page))

    return paginate_data(films_schema, films)


@categories_router.patch('/<category_id>/films/<film_id>')
def add_film(category_id, film_id):
    """
    :param category_id: The id of the category in the database
    :param film_id: The id of the film the actor will star in
    :return: The film object that has been added to the category, or an error message
    """
    category = Category.query.get_or_404(category_id)
    film = Film.query.get_or_404(film_id)
    category.films.append(film)
    db.session.commit()
    return film_schema.dump(film), 201


@categories_router.delete('/<category_id>/films/<film_id>')
def delete_film(category_id, film_id):
    """
    :param category_id: The id of the category in the database
    :param film_id: The id of the film the actor will star in
    :return: The film object that has been removed to the category, or an error message
    """
    category = Category.query.get_or_404(category_id)
    film = Film.query.get_or_404(film_id)
    category.films.remove(film)
    db.session.commit()
    return film_schema.dump(film), 201
