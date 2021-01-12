from flask import Blueprint, render_template
from . import db

server = Blueprint('server', __name__)

@server.route('/')
def index():
    return render_template('index.html')

@server.route('/profile')
def profile():
    return render_template('profile.html')