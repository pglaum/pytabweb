from flask import Blueprint, g, redirect, render_template, url_for
from datetime import datetime
from models.user import User
from pytz import timezone
from web import configuration
from web.forms.admin import AdminForm
import dateutil.parser
import json
import os

admin = Blueprint("admin", __name__)


@admin.route("/settings", methods=["GET", "POST"])
def settings():

    form = AdminForm()

    if form.validate_on_submit():

        g.config["registration_enabled"] = form.enable_registrations.data
        configuration.set(g.config)

    else:

        form.enable_registrations.data = g.config.get("registration_enabled", True)

    users = User.query.all()

    logs = None
    if os.path.isfile(g.config.get("log_file")):
        with open(g.config.get("log_file"), "r") as f:
            logs = json.loads(f.read())

    if logs:
        if "render" in logs:
            for entry in logs["render"]:
                t = dateutil.parser.isoparse(entry["time"])
                tz = timezone("UTC")
                t = t.replace(tzinfo=tz)
                entry["time"] = t.strftime("%Y-%m-%d %H:%M:%S")

        logs["render"].reverse()

    return render_template(
        "admin/settings.html", title="Admin Settings", form=form, users=users, logs=logs
    )


@admin.route("/logs/delete")
def logs_delete():

    os.remove(g.config.get("log_file"))

    return redirect(url_for("admin.settings"))
