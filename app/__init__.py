import os
from flask import Flask
from .db import db

def create_app(config='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

        from . import index
        app.register_blueprint(index.bp)

        return app
