from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from app import s3
from config import Config
from models.image import Image
from models.user import User

images_api_blueprint = Blueprint('images_api',
                             __name__,
                             template_folder='templates')


@images_api_blueprint.route('/', methods=['GET'])
def show():
    user_id = request.args.get('userId')
    if user_id:
        images = Image.select().where(Image.user_id == user_id)
        response = [image.image_path for image in images]
    else:
        response = [image.image_path for image in Image.select()]

    return jsonify(response)


@images_api_blueprint.route('/<id>/caption', methods=['GET'])
def caption(id):
    images = Image.select().where(Image.user_id == id)
    response = [{
        "id": image.id,
        "created_at": image.created_at,
        "caption": image.caption
    }
    for image in images]
    return jsonify(response)


# To test 
@images_api_blueprint.route('/', methods=['POST'])
@jwt_required
def create():
    current_user_id = get_jwt_identity()

    file = request.files.get('image')

    if file:
        try:
            s3.upload_fileobj(
                file,
                Config.S3_BUCKET,
                "user_images/" + file.filename,
                ExtraArgs={
                    "ACL": 'public-read',
                    "ContentType": file.content_type
                }
            )

            i = Image(image_name=file.filename, user=current_user_id, caption=caption)

            if i.save():
                return jsonify({
                    "image_path": i.image_path,
                    "success": True
                })

        except Exception as e:
            return jsonify({
                "error": e,
                "success": False
            })

    else:
        return jsonify({
            "message": "No image provided",
            "status": "failed"
        })


@images_api_blueprint.route('<image_id>/caption', methods=['POST'])
@jwt_required
def add_caption(image_id):
    i = Image.get(Image.id == image_id)
    i.caption = request.json.get('caption')

    if i.save():
        response = [{
            "id": i.id,
            "status": "success",
            "caption": i.caption
        }]
    else:
        response = [{
            "message": "Something went wrong",
            "status": "fail"
        }]

    return jsonify(response)
