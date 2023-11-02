from flask import Flask
from flask_migrate import Migrate

from .bundle.models import db

app = Flask(__name__)
app.secret_key = "TBDLATER_*#@&$%1"

# Flask-SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "mariadb+pymysql://root:you_wont_know_my_password@localhost/web-terminal"
db.init_app(app)

migrate = Migrate(app, db=db)

from .bundle.views import *