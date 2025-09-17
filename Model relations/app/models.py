from .extensions  import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
  id = db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(30), unique=True, nullable=False)
  first_name = db.Column(db.String(50), nullable=False)
  first_name = db.Column(db.String(50), nullable=True, default='Not Provided')
  email = db.Column(db.String(50), nullable=False, unique=True)
  phone = db.Column(db.String(15), nullable=False, unique=True)
  password_hash = db.Column(db.String(256), nullable=False)
  create_at = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default = datetime.utcnow, onupdate=datetime.utcnow)
  is_admin = db.Column(db.Boolean, default=False)
  
  def set_password(self, passowrd):
    self.password_hash = generate_password_hash(passowrd)
    
  def check_password_hash(self, password):
    return check_password_hash(self.password_hash, password)
  
  def __repr__(self):
    return '<User id={self.id}>'
  
    