
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.config import Settings

app = Flask(__name__)
app.config.from_object(Settings)
CORS(app)

# Connections
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Root Endpoint
@app.route(f'{app.config["APP_ROOT"]}/')
def root():
    return jsonify(message=f'Welcome to {app.config["APP_NAME"]}')

# Import the Blueprints
from app.auth.view import bp as auth_bp
from app.user.view import bp as users_bp
from app.pet.view import bp as pets_bp
from app.notification.view import bp as notifications_bp
from app.social_network.view import bp as social_network_bp

# Register the blueprint of the modules.
app.register_blueprint(auth_bp, url_prefix=f'{app.config["APP_ROOT"]}/auth')
app.register_blueprint(users_bp, url_prefix=f'{app.config["APP_ROOT"]}/users')
app.register_blueprint(pets_bp, url_prefix=f'{app.config["APP_ROOT"]}/pets')
app.register_blueprint(notifications_bp, url_prefix=f'{app.config["APP_ROOT"]}/notifications')
app.register_blueprint(social_network_bp, url_prefix=f'{app.config["APP_ROOT"]}/networks')
