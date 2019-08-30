from models.base_model import BaseModel
from models.user import User
import peewee as pw


class Image(BaseModel):
    image_name = pw.CharField()
    caption = pw.CharField(null = True)
    user = pw.ForeignKeyField(User, backref='images')
