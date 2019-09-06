from app import app
from flask_cors import CORS
from app import csrf

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from instagram_api.blueprints.users.views import users_api_blueprint


app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')

csrf.exempt(users_api_blueprint)