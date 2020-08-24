from flask import Blueprint, render_template, request, redirect
from app import db
from .db import Url
from .url_utils import get_short_url, check_url
from sqlalchemy.exc import IntegrityError
from .date_utils import now

from datetime import datetime

bp = Blueprint("index", __name__)


@bp.route("/")
@bp.route("/<short_url>")
def index(short_url=None):
    if short_url:
        query = Url.query.filter_by(short_url=short_url).first_or_404()

        if query.expiration_date and query.expiration_date < now():
            return {"error": "Expired"}, 400

        return redirect(query.url)

    return render_template("index.html")


@bp.route("/new", methods=["POST"])
def new():
    json = request.get_json()

    url = json.get("url")
    alias = json.get("alias")
    expiration_date = json.get("expiration_date")

    error = check_url(url)

    if error:
        return {"error": error}, 400

    short_url = get_short_url(url, alias=alias)

    if expiration_date:
        try:
            iso_date = datetime.fromisoformat(expiration_date)
            row = Url(url=url, short_url=short_url, expiration_date=iso_date)
        except ValueError:
            return {"error": f"{expiration_date} is not in ISO format"}, 400
    else:
        row = Url(url=url, short_url=short_url)

    try:
        db.session.add(row)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    return {"short_url": short_url}, 200
