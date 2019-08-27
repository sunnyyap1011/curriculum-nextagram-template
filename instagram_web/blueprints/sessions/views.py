from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import login_manager
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models.user import User


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

                            
@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    user = User.get_or_none(username=request.form.get('username'))

    if user != None:
        password_to_check = request.form.get('password')
        result = check_password_hash(user.password, password_to_check)

        if result == True:
            login_user(user)
            flash(f"You logged in successfully, {user.username}", 'success')
            return redirect(url_for('users.show', username=user.username))
        else:
            flash('Incorrect Password', 'danger')
            return render_template('sessions/new.html')

    else:
        flash('Username does not exist', 'danger')
        return render_template('sessions/new.html')


    return render_template('sessions/new.html')


@sessions_blueprint.route('/logout')
@login_required
def destroy():
    logout_user()
    flash("You've been logged out successfully", 'info')
    return redirect(url_for('sessions.new'))
