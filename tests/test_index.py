import html
import pytest

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
    assert response.json["shortUrl"] == "my-site"
    assert response.status_code == 200


def test_redirect_with_alias(client):
    response = client.get("/my-site")
    assert response.status_code == 302
    assert response.headers["Location"] == html.escape(URL)


EXPIRATION_DATE = "2020-01-02T22:50:00.000Z"


def test_new_with_expiration_date(client):
    response = client.post(
        "/new",
        json={
            "url": URL,
            "alias": "expired",
            "expirationDate": EXPIRATION_DATE,
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


def test_missing_short_url(client):
    response = client.get("/45123")
    assert response.status_code == 404


@pytest.mark.parametrize(
    ("url", "message"),
    (
        ("javascript:void(0)", "Unallowed URI scheme"),
        ("https://", "Invalid URL: no network location"),
    ),
)
def test_invalid_urls(client, url, message):
    response = client.post("/new", json={"url": url})
    assert response.status_code == 400
    assert response.json == {"error": message}


def test_new_non_iso_date(client):
    response = client.post(
        "/new", json={"url": URL, "alias": "expired", "expirationDate": "2020 13 August"},
    )
    assert response.status_code == 400
    assert response.json == {"error": "'2020 13 August' invalid ISO 8601 format"}
