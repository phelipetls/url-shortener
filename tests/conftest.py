import pytest

from app import create_app
from app.db import db as _db
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def env():
    load_dotenv()


@pytest.fixture(scope="session")
def app():
    return create_app("config.TestConfig")


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def db(app):
    with app.app_context():
        yield _db
        _db.drop_all()
