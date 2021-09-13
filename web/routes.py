from flask import g, render_template
from time import time
from web import app, configuration
from web.blueprints.admin import admin as admin_bp
from web.blueprints.auth import auth as auth_bp
from web.blueprints.main import main as main_bp
from web.blueprints.tabs import tabs as tabs_bp
from web.forms.tabs import SearchForm

app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(main_bp, url_prefix="/")
app.register_blueprint(tabs_bp, url_prefix="/tabs")


@app.before_request
def global_preparations():

    g.request_start_time = time()
    g.request_time = lambda: "%.3fs" % (time() - g.request_start_time)

    # TODO: test how this performs under load; maybe push config into a
    # database
    g.config = configuration.get()
    g.search_form = SearchForm()


@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404
