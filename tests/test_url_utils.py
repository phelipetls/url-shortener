import pytest
from app.url_utils import get_short_url


def test_url_shortener():
    """Should generate a random base64 encoded string with 6 chars."""
    short = get_short_url()
    assert isinstance(short, str)
    assert len(short) == 6


def test_url_shortener_with_alias():
    """Should return the alias."""
    assert get_short_url("alias") == "alias"


# vi: nowrap
