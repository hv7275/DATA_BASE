from flask import Blueprint, render_template, url_for, flash, redirect, current_app
from ..models import User
from ..extensions import db
from ..forms import RegistrationForm
from flask_login import login_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=["GET", 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    # if username already exists
    if User.query.filter_by(username = form.username.data).first():
      flash('Username already taken. Please choose another.', 'danger')
      return redirect(url_for('auth.register'))
    
    # if email already exist
    if User.query.filter_by(email = form.email.data).first():
      flash('Email already registered. Please log in.', 'danger')
      return redirect(url_for('auth.register'))
    
    if User.query.filter_by(phone=form.phone.data).first():
      flash('Phone number already registered.', 'danger')
      return redirect(url_for('auth.register'))
    
    # create new user
    
    new_user = User(
      username = form.username.data,
      first_name = form.first_name.data,
      last_name = form.last_name.data,
      email = form.email.data,
      phone = form.phone.data
    )
    
    new_user.set_password(form.password1.data)
    
    # Save to database
    try:
      db.session.add(new_user)
      db.session.commit()
      flash('Account created successfully! You can now log in.', 'success')
      login_user(new_user, remember=True)
      return redirect(url_for('main.home'))
    
    except Exception as e:
      db.session.rollback()
      current_app.logger.error("Registration failed: %s", e)
      flash('An error occurred while creating your account.', 'danger')
      return redirect(url_for('auth.register'))
  else:
    if form.is_submitted():
      print("VALIDATION FAILED:", form.errors)
  
  return render_template('register.html', form=form)
  