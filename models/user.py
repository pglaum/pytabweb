from flask_login import UserMixin
from web import db, login
from werkzeug.security import check_password_hash, generate_password_hash
import secrets


@login.user_loader
def load_user(id):
    """Load user by id."""

    return User.query.get(int(id))


@login.request_loader
def load_user_from_key(request):

    api_key = request.args.get('api_key')

    if api_key:

        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    return None


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    api_key = db.Column(db.Text, unique=True, default='')

    def __repr__(self):
        return f'<User: {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_api_key(self):
        self.api_key = secrets.token_urlsafe()
        db.session.commit()

    def remove_api_key(self):
        self.api_key = ''
        db.session.commit()
