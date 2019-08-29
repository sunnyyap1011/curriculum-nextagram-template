from models.base_model import BaseModel
from models.user import User
import peewee as pw


class Image(BaseModel):
    image_name = pw.CharField()
    caption = pw.CharField(null = True)
    user = pw.ForeignKeyField(User, backref='images')


# new folder?
# user_images
    # view.py
        # new - load the form for users to upload image_files
        # create - upload the images to AWS and database
        # edit - (e.g.caption) load the form for users to make changes the the image uploaded 
        # update - ['POST'] updtae the database
        # destroy - Delete the image