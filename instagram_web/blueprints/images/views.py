from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.image import Image
from app import s3
import os

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


@images_blueprint.route('/upload')
def new():
    return render_template('images/new.html')

@images_blueprint.route('/upload', methods=['POST'])
@login_required
def create():
    file = request.files.get('image')
    caption = request.form.get('caption')
    
    if file:
        try:
            s3.upload_fileobj(
                file,
                os.environ.get('S3_BUCKET'),
                "user_images/" + file.filename,
                ExtraArgs={
                    "ACL": 'public-read',
                    "ContentType": file.content_type
                }
            )

            i = Image(image_name=file.filename, user=current_user.id, caption=caption)

            if i.save():
                flash("Image uploaded successfully", 'success')
                return redirect(url_for('users.show', username=current_user.username))

        except Exception as e:
            flash(f"Something Happened: {e} ", 'danger')
            return redirect(url_for('users.show', username=current_user.username))

    else:
        return redirect(url_for('users.show', username=current_user.username))