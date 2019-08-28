from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import login_manager
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models.user import User



users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/sign_up', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    u = User(username=username, password=password, email=email)

    if u.save():
        flash(f"{u.username}, you've sign up successfully, please login to view your profile", 'success')
        return redirect(url_for('users.new'))
    else:
        flash(f'{u.errors[0]}', 'danger')
        return render_template('users/new.html')


@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    return render_template('users/show.html')


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    return render_template('users/edit.html', id=current_user.id)


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    new_username = request.form.get('username')
    new_email = request.form.get('email')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')

    user = User.get_by_id(id)


    if current_user == user:
        if new_username == user.username and new_email == user.email and not current_password and not new_password:
            flash("No change made to the user profile", 'info')
            return redirect(url_for('users.edit', id=id))

        if new_email != user.email:
            user.email = new_email

        if new_username != user.username:
            user.username = new_username

        if current_password and new_password:
            if check_password_hash(user.password, current_password):
                user.password = new_password

            else:
                flash('Invalid current password', 'danger')
                return redirect(url_for('users.edit', id=id))

        if user.save():
            flash("Your user profile have been updated successfully", 'success')
            return redirect(url_for('users.show', username=user.username))
        else:
            flash(f"{user.errors[0]}", 'danger')
            return redirect(url_for('users.edit', id=id))



    else:
        return redirect(url_for('users.login'))

    return redirect(url_for('users.show', username=user.username))



@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)