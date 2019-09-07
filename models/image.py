from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property
from config import Config
import peewee as pw


class Image(BaseModel):
    image_name = pw.CharField()
    caption = pw.CharField(null = True)
    user = pw.ForeignKeyField(User, backref='images')

    @hybrid_property
    def image_path(self):
        return Config.S3_LOCATION + "user_images/" + self.image_name