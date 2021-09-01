"""
Blueprint for guitar tab routes

"""

from datetime import datetime
from flask import (
    Blueprint,
    g,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import current_user, login_required
from hashlib import sha256
from models.tabs import GuitarTab
from web import app, db
from web.forms.tabs import EditForm, ReplaceFileForm, UploadForm
import json
import os

tabs = Blueprint("tabs", __name__)


@tabs.route("/render/<tab_id>")
def render(tab_id):

    tab = GuitarTab.query.filter_by(id=tab_id).first()
    if not tab:
        flash("Tab not found.", "danger")
        return redirect(url_for("main.index"))

    if not tab.views:
        tab.views = 1
    else:
        tab.views += 1
    db.session.commit()

    logs = {
        "render": [],
    }
    if os.path.isfile(g.config.get("log_file")):
        try:
            with open(g.config.get("log_file"), "r") as f:
                logs = json.loads(f.read())
                if not "render" in logs:
                    logs["render"] = []
        except Exception:
            pass

    username = "anonymous"
    if current_user.is_authenticated:
        username = current_user.username

    logs["render"].append(
        {
            "time": datetime.utcnow().isoformat(),
            "title": f"{tab.band} - {tab.song}",
            "user": username,
            "tabid": tab.id,
        }
    )
    with open(g.config.get("log_file"), "w") as f:
        f.write(json.dumps(logs))

    return render_template("tabs/render.html", title=f"{tab.song} - Tabs", tab=tab)


@tabs.route("/artist/<artist_name>")
def artist(artist_name):

    tabs_ = GuitarTab.query.filter_by(band=artist_name).order_by(GuitarTab.track).all()

    tabs = {}
    for t in tabs_:

        if t.album not in tabs:
            tabs[t.album] = [t]
        else:
            tabs[t.album].append(t)

    return render_template(
        "tabs/artist.html",
        title=f"Tabs by {artist_name}",
        artist_name=artist_name,
        tabs=tabs,
    )


@tabs.route("/get-tab/<tab_id>")
def get_tab(tab_id):

    tab = GuitarTab.query.filter_by(id=tab_id).first()
    if not tab:
        return "Not Found", 404

    filename = os.path.join(app.config.get("DATA_DIR"), tab.sha256 + tab.ext)
    if not os.path.isfile(filename):
        return "Not Found", 404

    return send_file(filename)


@login_required
@tabs.route("/upload", methods=["GET", "POST"])
def upload():

    if not current_user.is_authenticated:

        flash("You are not logged in.", "danger")
        return redirect(url_for("auth.login"))

    form = UploadForm()

    if form.validate_on_submit():

        f = request.files.get("upload_file")
        if not f:
            flash("No file was selected.", "warning")
            return redirect(url_for("tabs.upload"))

        data = f.stream.read()
        digest = sha256(data).hexdigest()
        existing = GuitarTab.query.filter_by(sha256=digest).first()

        if existing:

            flash("This file already exists", "warning")
            return redirect(url_for("tabs.render", tab_id=existing.id))

        else:

            ext = os.path.splitext(f.filename)[1]
            tab = GuitarTab(
                digest,
                ext,
                form.band.data,
                form.album.data,
                form.song.data,
                form.track.data,
            )

            filename = os.path.join(app.config.get("DATA_DIR"), tab.sha256 + tab.ext)
            with open(filename, "wb") as f:
                f.write(data)

            db.session.add(tab)
            db.session.commit()

            flash("File was uploaded", "success")
            return redirect(url_for("tabs.render", tab_id=tab.id))

    return render_template("tabs/upload.html", title="Upload a new tab", form=form)


@login_required
@tabs.route("/edit-metadata/<tab_id>", methods=["GET", "POST"])
def edit_metadata(tab_id):

    tab = GuitarTab.query.filter_by(id=tab_id).first()
    if not tab:
        flash("Tab not found.", "danger")
        return redirect(url_for("main.index"))

    form = EditForm()

    if form.validate_on_submit():

        tab.band = form.band.data
        tab.album = form.album.data
        tab.song = form.song.data
        tab.track = form.track.data
        db.session.commit()

        flash(f"Metadata for {tab.song} was saved.", "success")

        return redirect(url_for("tabs.render", tab_id=tab.id))

    else:

        form.band.data = tab.band
        form.album.data = tab.album
        form.song.data = tab.song
        form.track.data = tab.track

    return render_template(
        "tabs/edit-metadata.html",
        title=f"Edit metadata for {tab.song}",
        form=form,
        tab=tab,
    )


@login_required
@tabs.route("/delete/<tab_id>")
def delete(tab_id):

    if not current_user.is_authenticated or not current_user.is_admin:
        flash("Only an admin can delete tabs.", "danger")
        return redirect(url_for("tabs.render", tab_id=tab_id))

    tab = GuitarTab.query.filter_by(id=tab_id).first()
    if not tab:
        flash("Tab not found.", "danger")
        return redirect(url_for("main.index"))

    db.session.delete(tab)
    db.session.commit()

    flash("Tab was deleted.", "success")
    return redirect(url_for("main.index"))


@tabs.route("/download_gp/<tab_id>")
def download_gp(tab_id):

    tab = GuitarTab.query.filter_by(id=tab_id).first()
    if not tab:
        flash("Tab not found.", "danger")
        return redirect(url_for("main.index"))

    filename = os.path.join(app.config.get("DATA_DIR"), tab.sha256 + tab.ext)
    if not os.path.isfile(filename):
        return "Not Found", 404

    attachment_filename = f"{tab.band} - {tab.song}{tab.ext}"

    return send_file(
        filename, as_attachment=True, attachment_filename=attachment_filename
    )


@login_required
@tabs.route("/replace/<tab_id>")
def replace(tab_id):

    # TODO

    # upload a new guitar pro file for this tab
    tab = GuitarTab.query.filter_by(id=tab_id).first()
    if not tab:
        flash("Tab not found.", "danger")
        return redirect(url_for("main.index"))

    form = ReplaceFileForm()

    return render_template(
        "tabs/replace.html", title=f"Upload new tab for {tab.song}", form=form
    )
