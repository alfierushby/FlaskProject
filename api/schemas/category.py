from api.models.category import Category
from api.schemas import ma


# Auto-generate a schema for Film Models
class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category


# Instantiate the schema for both a single actor and many actors
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
