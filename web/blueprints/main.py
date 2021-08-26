"""
Blueprint for some general routes.

"""

from flask import Blueprint, render_template
from models.tabs import GuitarTab
from sqlalchemy import desc
from web.forms.tabs import SearchForm
from web.helpers import search_tabs

main = Blueprint("main", __name__)


@main.route("/")
def index():

    most_viewed = GuitarTab.query.order_by(desc(GuitarTab.views)).limit(5).all()
    recently_uploaded = (
        GuitarTab.query.order_by(desc(GuitarTab.date_added)).limit(5).all()
    )

    return render_template(
        "main/index.html",
        title="Guitar Tabs",
        recently_uploaded=recently_uploaded,
        most_viewed=most_viewed,
    )


@main.route("/search")
def search():

    form = SearchForm()

    query = form.q.data

    results = []
    if query:
        results = search_tabs(query)

    return render_template(
        "main/search.html",
        title="Guitar Tabs - Search",
        form=form,
        query=query,
        results=results,
    )


@main.route("/impressum")
def impressum():

    return render_template("main/impressum.html", title="Impressum")
