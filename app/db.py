from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False, unique=False)
    short_url = db.Column(db.String, nullable=False, unique=True)
    expiration_date = db.Column(db.DateTime, nullable=True)
