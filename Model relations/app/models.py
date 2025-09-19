from .extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
  __tablename__ = 'user'  # Optional: explicitly name the table
  
  id = db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(30), unique=True, nullable=False)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=True, default='Not Provided')
  email = db.Column(db.String(50), nullable=False, unique=True)
  phone = db.Column(db.String(15), nullable=False, unique=True)
  password_hash = db.Column(db.String(256), nullable=False)
  create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  is_admin = db.Column(db.Boolean, default=False)
  
  # Corrected one-to-many relationship
  # 'orders' (plural) holds all orders for this user.
  # backref='user' creates a .user attribute on the Order model.
  orders = db.relationship('Order', backref='user', lazy=True)
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
    
  # Renamed method to avoid shadowing the imported function
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  def __repr__(self):
    return f'<User {self.username}>'
  
class Order(db.Model):
  __tablename__ = 'order'  # Optional: explicitly name the table
  
  order_id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(50), nullable=True, unique=True)
  
  # Foreign key linking to the 'user' table's 'id' column.
  # Removed unique=True to allow a user to have multiple orders.
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
  price = db.Column(db.Integer(), nullable=False)
  
  # The relationship is now fully defined by the backref in the User model,
  # so the redundant definition here is removed.
  
  def __repr__(self):
    return f"<Order id: {self.order_id}>"