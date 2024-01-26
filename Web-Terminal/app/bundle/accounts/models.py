from app         import bcrypt
from app         import login_manager
from app         import db
from flask_login import UserMixin



@login_manager.user_loader
def user_loader(user_id):
  return User.query.get(int(user_id))


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True) 
  username = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  bio = db.Column(db.String(255))
  last_seen = db.Column(db.DateTime)
  pfp = db.Column(db.String(20), nullable=False, default="anonymous.png")

  def __init__(self, username: str, password: str) -> None:
    self.username = username
    self.password = bcrypt.generate_password_hash(password).decode("UTF-8")

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return str(self.id)
  
  def validate_pwd(self, pwd_to_validate):
    return bcrypt.check_password_hash(self.password, pwd_to_validate)
