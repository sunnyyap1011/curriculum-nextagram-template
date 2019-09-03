from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from instagram_web.blueprints.users.views import users_blueprint
from flask_login import login_required, current_user
from models.user import User
from models.following import Following


following_blueprint = Blueprint('following',
                            __name__,
                            template_folder='templates')


@following_blueprint.route('/follow/<id>', methods=['POST'])
def create(id):
    idol = User.get(User.id==id)

    f = Following(idol=idol.id, fan=current_user.id)

    if f.save():
        return jsonify({
            'success': True
        })
    else:
        return jsonify({
            'success': False
        })


@users_blueprint.route('<username>/following')
def show_following(username):
    user = User.get(username=username)
    return render_template('following/show.html', user=user)


@following_blueprint.route('/unfollow/<id>', methods=['POST'])
def destroy(id):
    idol = User.get(User.id==id)

    f = Following.get(idol=idol.id, fan=current_user.id)

    if f.delete_instance():
        flash(f"{current_user.username} has unfollow {idol.username}", 'success')
        return jsonify({
            'success': True
        })
    else:
        flash("Sorry, something went wrong, please try again", 'danger')
        return jsonify({
                    'success': False
                })

