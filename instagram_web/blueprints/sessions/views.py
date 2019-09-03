from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import login_manager
from instagram_web.blueprints.users.views import users_blueprint
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models.user import User
from instagram_web.helpers.google_oauth import oauth



sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

                            
@users_blueprint.route('/login', methods=['GET'])
def login():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/login', methods=['POST'])
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
            return redirect(url_for('users.login'))

    else:
        flash('Username does not exist', 'danger')
        return redirect(url_for('users.login'))


    return render_template('sessions/new.html')


@users_blueprint.route('/logout', methods=['POST'])
@login_required
def destroy():
    logout_user()
    flash("You've been logged out successfully", 'info')
    return redirect(url_for('users.login'))


@users_blueprint.route('/login/google', methods=['GET'])
def google_login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize/google')
def authorize():
    token = oauth.google.authorize_access_token()
    data = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()

    user = User.get_or_none(email=data['email'])

    if user != None:
        login_user(user)
        flash(f"You logged in successfully, {user.username}", 'success')
        return redirect(url_for('users.show', username=user.username))
    else:
        u = User(username=data['name'], email=data['email'], password='Abc123')
        if u.save():
            flash(f"{u.username}, you've sign up successfully, please login to view your profile", 'success')
            return redirect(url_for('users.show', username=u.username))
        else:
            flash(f'{u.errors[0]}', 'danger')
            return render_template('sessions/new.html')

    return redirect(url_for('users.new'))