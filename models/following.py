from models.base_model import BaseModel
from models.user import User
import re
import peewee as pw

class Following(BaseModel):
    fan = pw.ForeignKeyField(User, backref='idols')
    idol = pw.ForeignKeyField(User, backref='fans')
