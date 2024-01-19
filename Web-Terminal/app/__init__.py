from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('config')
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
api = Api(app)
jwt = JWTManager(app)

from .bundle.views import *
from .bundle.models import db

db.init_app(app)
migrate = Migrate(app, db)