from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import login_manager
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models.user import User


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    u = User(username=username, password=password, email=email)

    if u.save():
        flash(f'{u.username} successfully created', 'success')
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
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)