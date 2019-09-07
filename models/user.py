from models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask_login import UserMixin, current_user
from playhouse.hybrid import hybrid_property
from config import Config
import os
import re
import peewee as pw

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()
    profile_picture = pw.CharField()
    description = pw.TextField(null=True)
    status = pw.CharField(null=True)


    def validate(self):
        duplicate_users = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)
        email_regex = "^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$"
        password_regex = "^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,15}$"

        if not self.id and duplicate_users:
            self.errors.append('Username exists')
        if self.id and self.username != current_user.username and duplicate_users:
            self.errors.append('Username exists')    

        if not self.id and duplicate_email:
            self.errors.append('Email exists')
        if self.id and self.email != current_user.email and duplicate_email:
            self.errors.append('Email exists')    

        if not re.match(email_regex, self.email):
            self.errors.append('Please enter a valid email address')
            
        if self.id and self.password != current_user.password:
            if not re.match(password_regex, self.password):
                self.errors.append('New password must be at least 6 characters, no more than 15 characters, and must include at least one upper case letter, one lower case letter, and one numeric digit.')
            else:    
                self.password = generate_password_hash(self.password)

        if not self.id:
            if not re.match(password_regex, self.password):
                self.errors.append('Password must be at least 6 characters, no more than 15 characters, and must include at least one upper case letter, one lower case letter, and one numeric digit.')
            else:
                self.password = generate_password_hash(self.password)
        
        if not self.id:
            self.profile_picture = 'profile-placeholder.png'
            self.status = 'public'

    
    @hybrid_property
    def profile_picture_path(self):
        return Config.S3_LOCATION + self.profile_picture

    
    @hybrid_property
    def following(self):
        from models.fan_idol import Fan_Idol
        return [x.idol for x in Fan_Idol.select().where(Fan_Idol.fan_id == self.id).where(Fan_Idol.is_approved == True)]

    
    @hybrid_property
    def followers(self):
        from models.fan_idol import Fan_Idol
        return [x.fan for x in Fan_Idol.select().where(Fan_Idol.idol_id == self.id).where(Fan_Idol.is_approved == True)]


    @hybrid_property
    def following_request(self):
        from models.fan_idol import Fan_Idol
        return [x.idol for x in Fan_Idol.select().where(Fan_Idol.fan_id == self.id).where(Fan_Idol.is_approved == False)]

    
    @hybrid_property
    def followers_request(self):
        from models.fan_idol import Fan_Idol
        return [x.fan for x in Fan_Idol.select().where(Fan_Idol.idol_id == self.id).where(Fan_Idol.is_approved == False)]

    
    @hybrid_property
    def ordered_images(self):
        from models.image import Image
        return [x for x in Image.select().where(Image.user_id == self.id).order_by(Image.created_at.desc())]