# user_mgmt_system/__init__.py

# imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# app init
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

# DB setup
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@postgres-users/users"
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://pdogkmcqkaiono:88b8a26a9d4a00ff5a9acacfa984258051e83bbcb5e220e28ec9ed266f453a63@ec2-3-226-231-4.compute-1.amazonaws.com:5432/d4kmrclpsjjhm9"



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# login configs
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

# register blueprints
from user_mgmt_system.core.views import core
from user_mgmt_system.users.views import users
from user_mgmt_system.error_pages.error_handler import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
