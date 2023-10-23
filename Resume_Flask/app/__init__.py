from flask import Flask

app = Flask(__name__)
app.secret_key = "TBDLATER_*#@&$%1"

from .bundle.views import *