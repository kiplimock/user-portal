from user_mgmt_system import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(7))
    email = db.Column(db.String(100), nullable = False, unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f"Name: {self.first_name+' '+self.last_name}"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
