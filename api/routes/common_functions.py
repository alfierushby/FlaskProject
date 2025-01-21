from flask import request
from sqlalchemy import or_, and_

from api.models.actor import Actor


def paginate_args():
    return request.args.get('page', 1, type=int), request.args.get('per_page', 10, type=int)

def paginate_data(schema,entities):
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
    return entities.filter(and_(*[getattr(model,field).contains(f"%{value}%") for field, value in args if value]))
