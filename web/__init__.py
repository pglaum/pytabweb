from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

# initialize main components
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)

login.login_view = "auth.login"

from web import routes
