from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Feedback(db.Model):
  id = db.Column(db.Integer, primary_key=True) 
  username = db.Column(db.String(50))
  feedback = db.Column(db.String(255))
  date = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))
