from flask import render_template, request, url_for, redirect, Blueprint, abort, flash
from flask_login import login_user, logout_user, login_required, current_user
from user_mgmt_system import db
from user_mgmt_system.models import User
from user_mgmt_system.users.forms import RegistrationForm, LoginForm, EditUserForm

users = Blueprint('users', __name__)

# --------- USERS --------- #
@users.route('/users', methods=['GET','POST'])
def view_users():
    page = request.args.get('page',1,type=int)
    all_users = User.query.order_by(User.id.asc()).paginate(page=page, per_page=5, error_out=False)
    users = User.query.all()
    next_url = url_for('users.view_users', page=all_users.next_num) if all_users.has_next else None
    prev_url = url_for('users.view_users', page=all_users.prev_num) if all_users.has_prev else None
    return render_template('users.html', users=users, all_users=all_users.items, next_url=next_url, prev_url=prev_url)


# --------- REGISTER --------- #
@users.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name = form.name.data,
                    email = form.email.data,
                    gender = form.gender.data,
                    user_type = form.user_type.data,
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
        if user is None:
            flash("The email you entered is not registered!")
        else:
            if user.check_password(form.password.data):
                login_user(user)
                next = request.args.get('next')
                if next == None or not next[0] == '/':
                    next = url_for('core.index')
                return redirect(next)
            else:
                flash("The password you entered is invalid")
    return render_template('login.html', form=form)


# --------- LOG OUT --------- #
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route('/<int:user_id>/update', methods=["GET","POST"])
@login_required
def edit(user_id):
    form = EditUserForm()
    user = User.query.get(user_id)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.user_type = form.user_type.data
        db.session.commit()
        return redirect(url_for('core.index'))

    elif request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.user_type.data = user.user_type
    return render_template('edit_user.html', form=form, user=user)

# --------- DELETE --------- #
@users.route('/<int:user_id>/delete', methods=["GET","POST"])
@login_required
def delete(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('core.index'))
