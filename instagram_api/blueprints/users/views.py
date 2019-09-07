from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from werkzeug.security import check_password_hash
from models.user import User

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    response = [
        {'id': user.id,
         'username': user.username,
         'profile_picture': user.profile_picture_path,
         'description': user.description,
         'status': user.status
        } 
        for user in User.select()
        ]
    return jsonify(response)


@users_api_blueprint.route('/', methods=['POST'])
def create():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    u = User(username=username, password=password, email=email)

    if u.save():
        jwt = create_access_token(identity=u.id)
        response = {
            "jwt": jwt,
            "message": "Successfully created a user and signed in.",
            "status": "success",
            "user": {
                "id": u.id,
                "profile_picture": u.profile_picture_path,
                "username": u.username
            }       
        }
    else:
        response = {
            "message": [error for error in u.errors],
            "status": "failed"
        }
    return jsonify(response)
    

@users_api_blueprint.route('/<username>', methods=['GET'])
def show(username):
    user = User.get(username=username)
    if user:
        response = {
            'id': user.id,
            'username': user.username,
            'profile_picture': user.profile_picture_path,
            'description': user.description,
            'status': user.status
        }
    else:
        response = {
            "message": "User doesn't exist"
        } 
    return jsonify(response)


@users_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def me():
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "profile_picture": current_user.profile_picture_path,
        'description': current_user.description,
        'status': current_user.status
    })


@users_api_blueprint.route('/login', methods=['POST'])
def login():
    user = User.get_or_none(username=request.json.get('username'))

    if user != None:
        result = check_password_hash(user.password, request.json.get('password'))

        if result == True:
            jwt = create_access_token(identity=user.id)
            return jsonify({
                "jwt": jwt,
                "message": "Successfully signed in.",
                "status": "success",
                "user": {
                    "id": user.id,
                    "profile_picture": user.profile_picture_path,
                    "username": user.username
                }
            })
        else:
            return jsonify({
                "message": "Incorrect password.",
                "status": "fail"
                })
    else:
        return jsonify({
                "message": "Username not exist.",
                "status": "fail"
                })


@users_api_blueprint.route('/check_name', methods=['GET'])
def check_name():
    if User.get_or_none(User.username == request.args.get('username')) != None:
        return jsonify({
            "exists": True,
            "valid": False
        })
    else:
        return jsonify({
            "exists": False,
            "valid": True
        })