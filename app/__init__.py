from flask import Flask
from .db import db


def create_app(config="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

        from . import routes
        app.register_blueprint(routes.bp)

        return app
