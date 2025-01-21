from api.models import db


# A model of our actor table
class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    films = db.relationship('Film', secondary='film_category', back_populates='categories', lazy='dynamic')
