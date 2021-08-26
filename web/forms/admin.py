from flask_wtf import FlaskForm
from wtforms import BooleanField


class AdminForm(FlaskForm):

    enable_registrations = BooleanField("Enable registrations")
