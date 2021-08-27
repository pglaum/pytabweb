"""
Blueprint for the authentication process.

The first user has to be created from the cli.
All new users can be created by an admin.
"""

from flask import Blueprint, flash, g, render_template
from flask_login import current_user, login_user, logout_user
from models.user import User
from web import db
from web.forms.auth import LoginForm, RegistrationForm
from web.helpers import make_redirect

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """User login route."""

    # redirect to index, if the user is already logged in
    if current_user.is_authenticated:
        return make_redirect("main.index")

    form = LoginForm()
    if form.validate_on_submit():

        # validation is done by the login form
        user = User.query.filter_by(username=form.username.data).first()

        login_user(user, remember=form.remember_me.data)
        flash("Logged in.", "success")

        return make_redirect("main.index")

    return render_template("auth/login.html", title="Sign in", form=form)


@auth.route("/logout")
def logout():
    """Log the current user out."""

    logout_user()
    flash("Logged out.", "success")

    return make_redirect("main.index")


@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return make_redirect("main.index")

    form = RegistrationForm()

    if form.validate_on_submit():

        # validation is done by the registration form
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        users = User.query.all()
        if not users:
            user.is_admin = True

        db.session.add(user)
        db.session.commit()

        flash("Registration successful.", "success")

        return make_redirect("auth.login")

    return render_template(
        "auth/register.html",
        title="Register",
        form=form,
        registration_enabled=g.config.get("registration_enabled"),
    )
