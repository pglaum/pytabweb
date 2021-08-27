from flask_wtf import FlaskForm
from models.user import User
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")

    def validate(self):

        rv = FlaskForm.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.username.data).first()

        if user is None:
            message = (
                f'The user "{self.username.data}" does not exist. '
                '<a href="/auth/register">Click here</a> to create an account.'
            )
            self.username.errors.append(message)
            return False

        if not user.check_password(self.password.data):
            message = f'Invalid password for "{user.username}".'
            self.password.errors.append(message)
            return False

        return True


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat password", validators=[DataRequired(), EqualTo("password")]
    )

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.username.data).first()

        if user:
            message = "A user with this name already exists."
            self.username.errors.append(message)
            return False

        user = User.query.filter_by(email=self.email.data).first()

        if user:
            message = "This email address is already used."
            self.email.errors.append(message)
            return False

        return True
