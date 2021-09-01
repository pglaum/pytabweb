"""
Blueprint for some general routes.

"""

from flask import Blueprint, g, render_template
from flask_login import current_user, login_required
from models.tabs import Favorite, Tab
from sqlalchemy import desc
from web.forms.tabs import SearchForm
from web.helpers import search_tabs

main = Blueprint("main", __name__)


@main.route("/")
def index():

    most_viewed = Tab.query.order_by(desc(Tab.views)).limit(5).all()
    recently_uploaded = Tab.query.order_by(desc(Tab.date_added)).limit(5).all()

    favs = []
    if current_user.is_authenticated:
        favorites = Favorite.query.filter_by(user_id=current_user.id).all()
        favs = [f.tab_id for f in favorites]

    return render_template(
        "main/index.html",
        title="Guitar Tabs",
        recently_uploaded=recently_uploaded,
        most_viewed=most_viewed,
        favs=favs,
    )


@main.route("/search")
def search():

    query = g.search_form.q.data

    results = []
    favs = []
    if query:
        results = search_tabs(query)

        if current_user.is_authenticated:
            favorites = Favorite.query.filter_by(user_id=current_user.id).all()
            favs = [f.tab_id for f in favorites]

    return render_template(
        "main/search.html",
        title="Guitar Tabs - Search",
        query=query,
        results=results,
        favs=favs,
    )


@main.route("/impressum")
def impressum():

    return render_template("main/impressum.html", title="Impressum")


@login_required
@main.route("/favorites")
def favorites():

    favs = []
    if current_user.is_authenticated:
        favorites = Favorite.query.filter_by(user_id=current_user.id).all()
        favs = [f.tab_id for f in favorites]

    fav_tabs = []
    for fav in favs:
        tab = Tab.query.get(fav)
        if tab:
            fav_tabs.append(tab)

    return render_template(
        "main/favorites.html", title="Favorites", favs=favs, fav_tabs=fav_tabs
    )
