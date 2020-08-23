import re

import pytest
import html

from app.db import Url

URL = "https://google.com"


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_new(client, db):
    response = client.post("/new", json={"url": URL})
    assert response.status_code == 200


def test_new_with_alias(client, db):
    response = client.post("/new", json={"alias": "myalias", "url": URL})
    assert response.json["short_url"] == "myalias"
    assert response.status_code == 200


def test_new_already_shortened_url(client, db):
    response = client.post("/new", json={"url": URL})
    assert response.status_code == 200


def test_new_invalid_uri_schemes(client, db):
    response = client.post("/new", json={"url": "javascript:void(0)"})
    assert response.status_code == 400


def test_new_no_network_location(client, db):
    response = client.post("/new", json={"url": "https://"})
    assert response.status_code == 400


def test_redirect(client, db):
    short_url = Url.query.filter_by(url=URL).first().short_url

    response = client.get(f"/{short_url}")
    assert response.status_code == 302
    assert response.headers["Location"] == html.escape(URL)


def test_failed_redirect(client):
    response = client.get("/45123")
    assert response.status_code == 404
