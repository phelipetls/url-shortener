import re
import pytest
import html

from app.db import Url

URL = "https://google.com"


def test_home(client):
    """GET / should return 200 OK."""
    response = client.get("/")
    assert response.status_code == 200


def test_new(client, db):
    """POST /new should insert shorten and insert URL into database."""
    response = client.post("/new", json={"url": URL})
    assert response.status_code == 200


def test_new_with_alias(client, db):
    """POST /new with custom alias."""
    response = client.post("/new", json={"alias": "myalias", "url": URL})
    assert response.json["short_url"] == "myalias"
    assert response.status_code == 200


def test_new_already_shortened_url(client, db):
    """POST /new already shortened URL should not fail."""
    response = client.post("/new", json={"url": URL})
    assert response.status_code == 200


def test_redirect(client, db):
    """GET /<short_url> should return 302 FOUND (Redirect)."""
    short_url = Url.query.filter_by(url=URL).first().short_url

    response = client.get(f"/{short_url}")
    assert response.status_code == 302
    assert response.headers["Location"] == html.escape(URL)


def test_failed_redirect(client):
    """GET /<short_url> should return 404 NOT FOUND."""
    response = client.get("/45123")
    assert response.status_code == 404
