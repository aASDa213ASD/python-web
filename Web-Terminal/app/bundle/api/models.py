from app import db


class PhoneCall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caller = db.Column(db.String(50), nullable=False)
    recipient = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
