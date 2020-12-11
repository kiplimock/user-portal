from user_mgmt_system import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable = False, unique=True, index=True)
    gender = db.Column(db.String(7), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128))

    def __init__(self, name, email,gender, user_type, password):
        self.name = name
        self.email = email
        self.gender = gender
        self.user_type = user_type
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f"Name: {self.name}"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
