from . import db
from datetime import datetime


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False, unique=True)
    short_url = db.Column(db.String, nullable=False, unique=True)
