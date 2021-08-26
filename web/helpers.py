from flask import flash, redirect, request, url_for
from models.tabs import GuitarTab
from sqlalchemy import or_
from werkzeug.urls import url_parse


def make_redirect(default: str = "main.index") -> str:
    """Make a redirect or return the default."""

    next_page = request.args.get("next")
    if not next_page or url_parse(next_page).netloc != "":
        next_page = url_for(default)

    return redirect(next_page)


def search_tabs(query):

    results = []

    query = f"%{query}%"
    results = GuitarTab.query.filter(
        or_(
            GuitarTab.band.like(query),
            GuitarTab.album.like(query),
            GuitarTab.song.like(query),
        )
    ).all()

    return results
