from flask import Blueprint, render_template
from flask_login import login_required
import time

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
  return render_template('home.html', cache_buster=int(time.time()))


@main_bp.route('/')
@login_required
def admin():
  return render_template('admin.html')