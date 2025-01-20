from api.models import db
from api.models import film

# A model of our actor table
class Actor(db.Model):
    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)

    films = db.relationship('Film', secondary='film_actor',back_populates='actors')