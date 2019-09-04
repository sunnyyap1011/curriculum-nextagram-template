from models.base_model import BaseModel
from models.user import User
import peewee as pw

class Fan_Idol(BaseModel):
    fan = pw.ForeignKeyField(User, backref='idols')
    idol = pw.ForeignKeyField(User, backref='fans')
    is_approved = pw.BooleanField(null=True)