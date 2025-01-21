from api.models import db
from api.models import category

# A model of our film table
class Film(db.Model):
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=False)

    actors = db.relationship('Actor', secondary='film_actor', back_populates='films',lazy='dynamic')
    categories = db.relationship('Category', secondary='film_category', back_populates='films', lazy='dynamic')
