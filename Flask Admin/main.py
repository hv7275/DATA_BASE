from flask import Flask, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import (
    UserMixin, LoginManager,
    login_user, logout_user, current_user, login_required
)
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------------------------------
# 1. Initialize the Flask App and Database
# -------------------------------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sqlite.db"
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
db = SQLAlchemy(app)

# -------------------------------------------------
# 2. Setup Flask-Login
# -------------------------------------------------
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # redirect here if not logged in

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------------------------------------
# 3. Define the User Model
# -------------------------------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    items = db.relationship('Item', backref='owner', lazy=True)

    def __repr__(self):
        return f"Username: {self.name}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# -------------------------------------------------
# 4. Secure Flask-Admin Views
# -------------------------------------------------
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to login if not authorized
        return redirect(url_for('login', next=request.url))

# -------------------------------------------------
# 5. Setup Flask-Admin
# -------------------------------------------------
admin = Admin(app, name='My Dashboard', template_mode='bootstrap4')
admin.add_view(SecureModelView(User, db.session))

# -------------------------------------------------
# 6. Routes
# -------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("admin.index"))
        else:
            flash("Invalid email or password")
    return '''
        <h2>Login</h2>
        <form method="post">
            Email: <input type="text" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# -------------------------------------------------
# 7. Database Initialization
# -------------------------------------------------
with app.app_context():
    db.create_all()

    # Create default admin user if it doesn't exist
    if not User.query.filter_by(email="owner@example.com").first():
        u = User(name="Owner", email="owner@example.com", is_admin=True)
        u.set_password("supersecret")
        db.session.add(u)
        db.session.commit()

# -------------------------------------------------
# 8. Run the App
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)