from models.base_model import BaseModel
from werkzeug.security import generate_password_hash
import peewee as pw
import re

class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()

    def validate(self):
        duplicate_users = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)
        password_regex = "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,15}$"

        if duplicate_users:
            self.errors.append('Username exists')
        if duplicate_email:
            self.errors.append('Email exists')
        if not re.match(password_regex, self.password):
            self.errors.append('Password must be at least 6 characters, no more than 15 characters, and must include at least one upper case letter, one lower case letter, and one numeric digit.')
        if not self.id:
            self.password = generate_password_hash(self.password)

            