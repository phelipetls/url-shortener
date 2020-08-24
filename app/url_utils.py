from secrets import token_urlsafe
from urllib.parse import urlparse


def check_url(url):
    parsed_url = urlparse(url)

    scheme = parsed_url.scheme
    netloc = parsed_url.netloc

    if scheme in ["data", "javascript"]:
        return "Unallowed URI scheme"

    if not netloc:
        return "Invalid URL: no network location"


def get_short_url(alias=None):
    if alias:
        short_string = alias
    else:
        short_string = token_urlsafe(4)
    return short_string
