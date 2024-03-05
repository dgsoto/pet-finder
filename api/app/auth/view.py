from datetime import datetime

from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, create_access_token, current_user, get_jwt

from app import db
from app.user.models import User
from app.user.schemas import user_schema
from app.auth.handlers import *


bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
def register():
    """
    Endpoint POST http://127.0.0.1:5000/api/auth/register to create a new user.

    Required:
    - username      (str)   Unique username.
    - email         (str)   Unique email.
    - password      (str)   Password of the user.
    - first_name    (str)   Name of the user.
    - last_name     (str)   Lastname of the user.
    - address       (str)   Address of the user.

    Optional:
    - avatar_url    (str)   User url image.

    Return:
    - user_data     (dict)  Created user data.
    """
    # Load the data of the request using the schema UserSchema
    user_schema_ref = user_schema
    data = request.json
    try:
        data["password"] = generate_password_hash(data.get("password"))
        validated_data = user_schema_ref.load(data)

        db.session.add(validated_data)
        db.session.commit()

        # Return the user object created as part of the response.
        user_data = user_schema.dump(validated_data)
        return jsonify(user_data), 200
    except ValidationError as err:
        # Manage the errors of validation and return a message according specific error.
        return jsonify(err.messages), 400


@bp.route("/login", methods=["POST"])
def login():
    """
    Endpoint POST /api/auth/login to authenticate a user and get an access token.

    Required:
    - username      (str)   Username of the user.
    - password      (str)   Password of the user.

    Return:
    - access_token  (str)   JWT access token for authentication.
    """
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify(message="Username and password are required"), 400

    # Get user in database
    user = User.query.filter_by(username=username).first()

    # Verify user and password
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)
        return jsonify({"access_token": access_token})

    return jsonify(message="Invalid username or password"), 401


@bp.route("/verify", methods=["GET"])
@jwt_required()
def verify():
    """
    Endpoint GET /api/auth/verify to verify the JWT access token.

    Return:
    - message       (str)   Message indicating successful verification.
    """
    return jsonify(message=f"Verify endpoint for {current_user.username}")
