from flask import render_template, Blueprint
from user_mgmt_system import db, app

core = Blueprint('core', __name__)

# --------- HOME --------- #
@core.route('/')
def index():
    db.create_all()
    return render_template('index.html')


# --------- ABOUT --------- #
@core.route('/about')
def info():
    return render_template('about.html')


# --------- CONTACT --------- #
@core.route('/contact')
def contact():
    return render_template('contact.html')
