from flask import request

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