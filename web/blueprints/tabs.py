"""
Blueprint for guitar tab routes

"""

from flask import Blueprint, flash, redirect, render_template, request, \
    send_file, url_for
from flask_login import current_user, login_required
from hashlib import sha256
from models.tabs import GuitarTab
from web import app, db
from web.forms.tabs import EditForm, ReplaceFileForm, UploadForm
import os

tabs = Blueprint('tabs', __name__)


@tabs.route('/render/<tab_id>')
def render(tab_id):

    tab = GuitarTab.query.filter_by(id=tab_id).first()
    if not tab:
        flash('Tab not found.', 'danger')
        return redirect(url_for('main.index'))

    if not tab.views:
        tab.views = 1
    else:
        tab.views += 1
    db.session.commit()

    return render_template('tabs/render.html', tab=tab)


@tabs.route('/artist/<artist_name>')
def artist(artist_name):

    tabs_ = GuitarTab.query \
        .filter_by(band=artist_name) \
        .order_by(GuitarTab.track) \
        .all()

    tabs = {}
    for t in tabs_:

        if t.album not in tabs:
            tabs[t.album] = [t]
        else:
            tabs[t.album].append(t)

    return render_template('tabs/artist.html', artist_name=artist_name,
                           tabs=tabs)


@tabs.route('/get-tab/<tab_id>')
def get_tab(tab_id):

    tab = GuitarTab.query.filter_by(id=tab_id).first()
    if not tab:
        return "Not Found", 404

    filename = os.path.join(app.config.get('DATA_DIR'), tab.sha256 + tab.ext)
    if not os.path.isfile(filename):
        return "Not Found", 404

    return send_file(filename)


@login_required
@tabs.route('/upload', methods=['GET', 'POST'])
def upload():

    if not current_user.is_authenticated:

        flash('You are not logged in.', 'danger')
        return redirect(url_for('main.index'))

    form = UploadForm()

    if form.validate_on_submit():

        f = request.files.get('upload_file')
        if not f:
            flash('No file was selected.', 'warning')
            return redirect(url_for('tabs.upload'))

        data = f.stream.read()
        digest = sha256(data).hexdigest()
        existing = GuitarTab.query.filter_by(sha256=digest).first()

        if existing:

            flash('This file already exists', 'warning')
            return redirect(url_for('tabs.render', tab_id=existing.id))

        else:

            ext = os.path.splitext(f.filename)[1]
            tab = GuitarTab(digest, ext, form.band.data, form.album.data,
                            form.song.data, form.track.data)

            filename = os.path.join(app.config.get('DATA_DIR'),
                                    tab.sha256 + tab.ext)
            with open(filename, 'wb') as f:
                f.write(data)

            db.session.add(tab)
            db.session.commit()

            flash('File was uploaded', 'success')
            return redirect(url_for('tabs.render', tab_id=tab.id))

    return render_template('tabs/upload.html', form=form)


@login_required
@tabs.route('/delete/<tab_id>')
def delete(tab_id):

    tab = GuitarTab.query.filter_by(id=tab_id).first()
    if not tab:
        flash('Tab not found.', 'danger')
        return redirect(url_for('main.index'))

    db.session.delete(tab)
    db.session.commit()

    flash('Tab was deleted.', 'success')
    return redirect(url_for('main.index'))


@tabs.route('/download_gp/<tab_id>')
def download_gp(tab_id):

    tab = GuitarTab.query.filter_by(id=tab_id).first()
    if not tab:
        flash('Tab not found.', 'danger')
        return redirect(url_for('main.index'))

    filename = os.path.join(app.config.get('DATA_DIR'), tab.sha256 + tab.ext)
    if not os.path.isfile(filename):
        return "Not Found", 404

    attachment_filename = f'{tab.band} - {tab.song}{tab.ext}'

    return send_file(filename, as_attachment=True,
                     attachment_filename=attachment_filename)


@login_required
@tabs.route('/replace/<tab_id>')
def replace(tab_id):

    # upload a new guitar pro file for this tab
    tab = GuitarTab.query.filter_by(id=tab_id).first()
    if not tab:
        flash('Tab not found.', 'danger')
        return redirect(url_for('main.index'))

    form = ReplaceFileForm()
    cur_filename = os.path.join(app.config.get('DATA_DIR'),
                                tab.sha256 + tab.ext)

    return render_template('tabs/replace.html', form=form)
