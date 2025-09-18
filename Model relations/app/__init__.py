import os
from flask import Flask
from .extensions import db, csrf, migrate, login_manager, admin
from dotenv import load_dotenv  
from .models import User

# Load environment variables from the .env file
load_dotenv()

def create_app():
  app = Flask(__name__, static_folder='static')
  # Enable fast iteration in development: auto-reload templates and disable static caching
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.jinja_env.auto_reload = True
  app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
  
  SECRET_KEY = os.getenv('SECRET_KEY')
  DATABASE_URI = os.getenv('DATABASE_URI')
  
  if not SECRET_KEY or not DATABASE_URI:
      raise ValueError("SECRET_KEY and DATABASE environment variables must be set.")
      
  app.config['SECRET_KEY'] = SECRET_KEY
  app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
  
  db.init_app(app)
  csrf.init_app(app)
  migrate.init_app(app, db)
  login_manager.init_app(app)
  login_manager.login_view = 'auth.login'
  admin.init_app(app)
  
  
  # user loader 
  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))
  
  # Register blueprints
  from .routes.auth_routes import auth_bp
  from .routes.main_routes import main_bp
  app.register_blueprint(main_bp)
  app.register_blueprint(auth_bp)
  
  return app