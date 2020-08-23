import re
import pytest
from app import create_app


def test_config_development():
    app = create_app()
    assert not app.testing
    assert "postgres" in app.config["SQLALCHEMY_DATABASE_URI"]


def test_config_testing():
    app = create_app("config.TestConfig")
    assert app.testing
    assert re.match("sqlite:////tmp/", app.config["SQLALCHEMY_DATABASE_URI"])
