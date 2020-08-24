import html

from app.db import Url
from datetime import datetime
from freezegun import freeze_time

URL = "https://google.com"


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_new(client):
    response = client.post("/new", json={"url": URL})
    assert response.status_code == 200


def test_redirect(client, db):
    short_url = Url.query.filter_by(url=URL).first().short_url

    response = client.get(f"/{short_url}")
    assert response.status_code == 302
    assert response.headers["Location"] == html.escape(URL)


def test_new_with_alias(client):
    response = client.post("/new", json={"alias": "my-site", "url": URL})
    assert response.json["short_url"] == "my-site"
    assert response.status_code == 200


def test_redirect_with_alias(client):
    response = client.get("/my-site")
    assert response.status_code == 302
    assert response.headers["Location"] == html.escape(URL)


EXPIRATION_DATE = datetime(2020, 1, 2)


def test_new_with_expiration_date(client):
    response = client.post(
        "/new",
        json={
            "url": URL,
            "alias": "expired",
            "expiration_date": EXPIRATION_DATE.isoformat(),
        },
    )
    assert response.status_code == 200


@freeze_time("2020-01-01")
def test_redirect_link_unexpired(client):
    response = client.get("/expired")
    assert response.status_code == 302


def test_redirect_link_expired(client):
    response = client.get("/expired")
    assert response.status_code == 400
    assert "error" in response.json


def test_already_shortened_url(client):
    response = client.post("/new", json={"url": URL})
    assert response.status_code == 200


def test_invalid_uri_schemes(client):
    response = client.post("/new", json={"url": "javascript:void(0)"})
    assert response.status_code == 400


def test_no_network_location(client):
    response = client.post("/new", json={"url": "https://"})
    assert response.status_code == 400


def test_missing_short_url(client):
    response = client.get("/45123")
    assert response.status_code == 404
