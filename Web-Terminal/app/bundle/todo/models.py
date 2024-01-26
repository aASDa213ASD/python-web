from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import bcrypt
from app import login_manager
from app import db


class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer)
  title = db.Column(db.String(100))
  description = db.Column(db.String(200))
  due_date = db.Column(db.Date())
  status = db.Column(db.Boolean)
