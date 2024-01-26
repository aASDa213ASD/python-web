from flask import Blueprint


api_todo = Blueprint("api_todo", __name__, url_prefix="/api")
api_accounts = Blueprint("api_accounts", __name__, url_prefix="/api")
