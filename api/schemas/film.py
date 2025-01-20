from api.models.film import Film
from api.schemas import ma


# Auto-generate a schema for Film Models
class FilmSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Film


# Instantiate the schema for both a single actor and many actors
film_schema = FilmSchema()
films_schema = FilmSchema(many=True)
