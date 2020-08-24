import re

import pytest
import html

from app.db import Url
from datetime import datetime, timedelta

URL = "https://google.com"


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_new(client, db):
    response = client.post("/new", json={"url": URL})
    assert response.status_code == 200


def test_redirect(client, db):
    short_url = Url.query.filter_by(url=URL).first().short_url

    response = client.get(f"/{short_url}")
    assert response.status_code == 302
    assert response.headers["Location"] == html.escape(URL)


def test_new_with_alias(client, db):
    response = client.post("/new", json={"alias": "my-site", "url": URL})
    assert response.json["short_url"] == "my-site"
    assert response.status_code == 200


def test_redirect_with_alias(client, db):
    response = client.get("/my-site")
    assert response.status_code == 302
    assert response.headers["Location"] == html.escape(URL)


def test_new_with_expiration_date(client, db):
    expiration_date = datetime(2020, 1, 2)
    response = client.post(
        "/new",
        json={
            "url": URL,
            "alias": "expired",
            "expiration_date": expiration_date.isoformat(),
        },
    )
    assert response.status_code == 200


def test_redirect_link_not_yet_expired(mocked_now, client, db):
    response = client.get("/expired")
    assert response.status_code == 302


def test_redirect_link_expired(client, db):
    response = client.get("/expired")
    assert response.status_code == 400
    assert "error" in response.json


def test_already_shortened_url(client, db):
    response = client.post("/new", json={"url": URL})
    assert response.status_code == 200


def test_invalid_uri_schemes(client, db):
    response = client.post("/new", json={"url": "javascript:void(0)"})
    assert response.status_code == 400


def test_no_network_location(client, db):
    response = client.post("/new", json={"url": "https://"})
    assert response.status_code == 400


def test_missing_short_url(client):
    response = client.get("/45123")
    assert response.status_code == 404
