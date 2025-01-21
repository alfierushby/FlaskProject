from flask import request
from sqlalchemy import and_

from api.models.actor import Actor


def paginate_args():
    return request.args.get('page', 1, type=int), request.args.get('per_page', 10, type=int)

def paginate_data(schema,entities):
    """
    :param schema: The relevant schema for the entities
    :param entities: The database entities
    :return: Paginated data for the entities
    """
    data = {
        "data": schema.dump(entities),
        "total": entities.total,
        "pages": entities.pages,
        "current_page": entities.page,
        "per_page": entities.per_page
    }

    if entities.page < entities.pages:
        data["next_page"] = f"{request.base_url}?page={entities.page + 1}"

    if entities.page > 1:
        data["prev_page"] = f"{request.base_url}?page={entities.page - 1}"
    return data

def filter_data(entities,model,args):
    """
    :param entities: The database entities to filter
    :param model: The database model for the entities
    :param args: The arguments to filter in [(field,value),...] form.
    :return: The filtered entities
    """
    return entities.filter(and_(*[getattr(model,field).contains(f"%{value}%") for field, value in args if value]))
