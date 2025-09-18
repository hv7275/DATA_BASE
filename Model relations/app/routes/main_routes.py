from flask import Blueprint, render_template
import time

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
  return render_template('home.html', cache_buster=int(time.time()))
