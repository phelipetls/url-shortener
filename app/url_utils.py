from hashlib import md5
from base64 import b32encode
from urllib.parse import urlparse
from datetime import datetime


def check_url(url):
    parsed_url = urlparse(url)

    scheme = parsed_url.scheme
    netloc = parsed_url.netloc

    if not netloc:
        return "Invalid URL: no network location"

    if scheme in ["data", "javascript"]:
        return "Unallowed URI scheme".format(scheme)


def get_short_url(url, alias=None):
    if alias:
        short_string = alias
    else:
        hashed = md5(url.encode())
        b32encoded = b32encode(hashed.digest())
        short_string = b32encoded.decode()[:6]
    return short_string
