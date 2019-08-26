from flask import Blueprint, render_template, request, redirect, url_for, flash
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
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
