import re
import pytest
import html

from app.models import Url

URL = "https://google.com"


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_new(client, db):
    """Should insert a new short url inside the table Url."""
    response = client.post("/new", json={"url": URL})

    assert "short_url" in response.json
    assert response.status_code == 200


def test_redirect(client, db):
    short_url = Url.query.filter_by(url=URL).first().short_url

    response = client.get(f"/{short_url}")

    assert response.status_code == 302
    assert response.headers["Location"] == html.escape(URL)


def test_failed_redirect(client):
    response = client.get("/45123")

    assert response.status_code == 404
