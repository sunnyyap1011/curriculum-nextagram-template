import os
import config
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from models.base_model import db
from config import Config
import boto3, botocore
import braintree
from flask_jwt_extended import JWTManager

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

app.secret_key = b'\xa7\xc4\xa2\x8f\xf7\x98S\x11\xd5*z4D\xfb\xb5\x83'

login_manager = LoginManager()
login_manager.init_app(app)

csrf = CSRFProtect(app)

jwt = JWTManager(app)

s3 = boto3.client(
   "s3",
   aws_access_key_id=Config.S3_KEY,
   aws_secret_access_key=Config.S3_SECRET
)

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=Config.BRAINTREE_MERCHANT_ID,
        public_key=Config.BRAINTREE_PUBLIC_KEY,
        private_key=Config.BRAINTREE_PRIVATE_KEY
    )
)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
