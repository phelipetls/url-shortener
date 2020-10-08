import re
from app import create_app


def test_config_development():
    app = create_app()
    assert not app.testing
    assert app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgresql+psycopg2")


def test_config_testing():
    app = create_app("config.TestConfig")
    assert app.testing
    assert app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:////tmp/")
