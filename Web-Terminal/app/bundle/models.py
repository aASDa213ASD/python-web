from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Feedback(db.Model):
  id = db.Column(db.Integer, primary_key=True) 
  username = db.Column(db.String(50))
  feedback = db.Column(db.String(255))
  date = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True) 
  username = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer)
  title = db.Column(db.String(100))
  description = db.Column(db.String(200))
  due_date = db.Column(db.Date())
  status = db.Column(db.Boolean)