from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from instagram_web.blueprints.users.views import users_blueprint
from flask_login import login_required, current_user
from models.user import User
from models.fan_idol import Fan_Idol


following_blueprint = Blueprint('following',
                            __name__,
                            template_folder='templates')


@following_blueprint.route('/follow/<id>', methods=['POST'])
def create(id):
    idol = User.get(User.id==id)

    f = Fan_Idol(idol=idol.id, fan=current_user.id)
    

    if f.save():
        followers_count = len(idol.fans)
        return jsonify({
            'success': True,
            'followers_count': followers_count
        })
    else:
        return jsonify({
            'success': False
        })


@users_blueprint.route('<username>/following')
def show_following(username):
    user = User.get(username=username)
    return render_template('following/show_following.html', user=user)


@users_blueprint.route('<username>/followers')
def show_followers(username):
    user = User.get(username=username)
    return render_template('following/show_followers.html', user=user)


@following_blueprint.route('/unfollow/<id>', methods=['POST'])
def destroy(id):
    idol = User.get(User.id==id)

    f = Fan_Idol.get(idol=idol.id, fan=current_user.id)


    if f.delete_instance():
        followers_count = len(idol.fans)
        return jsonify({
            'success': True,
            'followers_count': followers_count
        })
    else:
        return jsonify({
                    'success': False
                })

