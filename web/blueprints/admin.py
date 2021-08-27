from flask import Blueprint, g, render_template
from models.user import User
from web import configuration
from web.forms.admin import AdminForm

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

    return render_template(
        "admin/settings.html", title="Admin Settings", form=form, users=users
    )
