from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

film_actor = db.Table('film_actor',
                      db.Column('actor_id', db.Integer, db.ForeignKey('actor.actor_id'), primary_key=True),
                      db.Column('film_id', db.Integer, db.ForeignKey('film.film_id'), primary_key=True),
                      db.Column('last_update', db.Date))

film_category = db.Table('film_category',
                         db.Column('category_id', db.Integer, db.ForeignKey('category.category_id'), primary_key=True),
                         db.Column('film_id', db.Integer, db.ForeignKey('film.film_id'), primary_key=True),
                         db.Column('last_update', db.Date))
