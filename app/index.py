from flask import Blueprint, render_template, request, redirect
from app import db
from .db import Url
from .url_utils import get_short_url, check_url
from sqlalchemy.exc import IntegrityError

bp = Blueprint("index", __name__)


@bp.route("/")
@bp.route("/<short_url>")
def index(short_url=None):
    if short_url:
        query = Url.query.filter_by(short_url=short_url).first_or_404()
        return redirect(query.url)

    return render_template("index.html")


@bp.route("/new", methods=["POST"])
def new():
    json = request.get_json()

    url = json.get("url")
    alias = json.get("alias")

    error = check_url(url)

    if error:
        return {"error": error}, 400

    short_url = get_short_url(url, alias=alias)

    new_row = Url(url=url, short_url=short_url)

    try:
        db.session.add(new_row)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    return {"short_url": short_url}, 200
