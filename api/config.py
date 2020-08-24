import os
import tempfile


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class TestConfig:
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    _, filename = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{filename}"
