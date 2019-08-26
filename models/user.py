from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()