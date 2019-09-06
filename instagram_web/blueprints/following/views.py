from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from instagram_web.blueprints.users.views import users_blueprint
from flask_login import login_required, current_user
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import urllib.parse
import os
from models.user import User
from models.fan_idol import Fan_Idol


following_blueprint = Blueprint('following',
                            __name__,
                            template_folder='templates')


@following_blueprint.route('/follow/<id>', methods=['POST'])
def create(id):
    idol = User.get(User.id==id)

    if idol.status == 'public':
        f = Fan_Idol(idol=idol.id, fan=current_user.id, is_approved=True)
    else:
        f = Fan_Idol(idol=idol.id, fan=current_user.id, is_approved=False)
        encode_username = urllib.parse.quote(idol.username)

        message = Mail(
            from_email='nextagram@example.com',
            to_emails= idol.email,
            subject=f"Following request from {current_user.username}",
            html_content=f"Hi, {idol.username}! <br /><br /> Click on the link below to approve the follow request <br /> {request.url_root}users/{encode_username}/followers "
        )
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(str(e))
    

    if f.save():
        followers_count = len(idol.followers)
        if f.is_approved == False:
            return jsonify({
                'success': True,
                'followers_count': followers_count,
                'status': 'pending'
            })
        else:
            return jsonify({
                'success': True,
                'followers_count': followers_count,
                'status': 'approved'
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

    if idol.status == 'private':
        is_private = True
    else:
        is_private = False

    if f.delete_instance():
        followers_count = len(idol.followers)
        private_container = render_template('private_container.html')
        return jsonify({
            'success': True,
            'followers_count': followers_count,
            'private_container': private_container,
            'is_private': is_private
        })
    else:
        return jsonify({
                    'success': False
                })


@users_blueprint.route('approve_followers/<username>', methods=['POST'])
@login_required
def approve_followers(username):
    user = User.get(username=username)
    x = Fan_Idol.get(idol=current_user.id, fan=user.id)
    
    x.is_approved = True

    if x.save():
        flash(f"You have approved the following request from {user.username} ", 'success')
        return redirect(url_for('users.show_followers', username=current_user.username))


@users_blueprint.route('reject_followers/<username>', methods=['POST'])
@login_required
def reject_followers(username):
    user = User.get(username=username)

    f = Fan_Idol.get(idol=current_user.id, fan=user.id)
    
    if f.delete_instance():
        flash(f"You have reject request from {user.username} ", 'danger')
        return redirect(url_for('users.show_followers', username=current_user.username))