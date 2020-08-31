from flask import render_template, request, url_for, redirect, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from user_mgmt_system import db
from user_mgmt_system.models import User
from user_mgmt_system.users.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)

@users.route('/users', methods=['GET','POST'])
@login_required
def view_users():
    page = request.args.get('page',1,type=int)
    name = current_user.first_name+' '+current_user.last_name
    users = User.query.order_by(User.first_name.asc()).paginate(page=page, per_page=10)
    return render_template('users.html', name=name, users=users)

# --------- REGISTER --------- #
@users.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    email = form.email.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

# --------- LOG IN --------- #
@users.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('core.index')
            return redirect(next)
    return render_template('login.html', form=form)

# --------- LOG OUT --------- #
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))
