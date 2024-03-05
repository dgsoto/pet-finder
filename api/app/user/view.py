from flask import Blueprint, jsonify, request
from datetime import datetime
from app import db
from app.user.models import User
from app.user.schemas import user_schema, users_schema
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
import re

bp = Blueprint('users', __name__)

@bp.route('/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
    Endpoint GET http://127.0.0.1:5000/api/users/<string:user_id> to get a user by ID.
    
    Required:
    - user_id       (str)   Unique user id.

    Return:
    - user_data     (dict)  User data.
    """
    # Find the user by ID
    try:
        # Query to search an user by id in the database.
        user = User.query.filter_by(id=user_id).first()

        # If the user is not found, return a 404 Not Found.
        if not user:
            return jsonify(message="Usuario no encontrado"), 404

        # Serialize the user and return it as a response.
        user_data = user_schema.dump(user)
        return jsonify(user_data), 200
    except ValueError:
        raise BadRequest("ID de usuario inválido")
    except ValidationError as err:
        # Handle schema validation errors.
        return jsonify(err.messages), 400

@bp.route('/', methods=['GET'])
def get_users():
    """
    Endpoint GET to list the users with pagination.
    Examples:
    - http://127.0.0.1:5000/api/users
    - http://127.0.0.1:5000/api/users?page=1&per_page=5

    Query Parameters:
    - page      (int)   Page number (default 1).
    - per_page  (int)   Number of users per page (default 5).

    Return:
    - users_data (list)  List of users on the specified page.
    """
    try:
        # Pagination parameters.
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))

        # Query to get paged users.
        users = User.query.paginate(page=page, per_page=per_page)

        # Serialize results.
        users_data = users_schema.dump(users.items)

        # Build paginated response.
        response = {
            "users": users_data,
            "total_pages": users.pages,
            "total_users": users.total,
            "current_page": page
        }

        return jsonify(response), 200
    except Exception as e:
        # Handle the error and return an appropriate error message.
        return jsonify({"message": "Error al listar usuarios.", "error": str(e)}), 500

@bp.route('/<string:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    """
    Endpoint DELETE http://127.0.0.1:5000/api/users/<string:user_id> to delete a user by ID.
    
    Required:
    - user_id       (str)   Unique user id.

    Return:
    - message      (str)   Success or error message.
    """
    try:
        # Search the user by ID.
        user = User.query.filter_by(id=user_id).first()

        # If the user is not found, return a 404 error.
        if not user:
            return jsonify(message="Usuario no encontrado."), 404

        # Delete the user from the database.
        db.session.delete(user)
        db.session.commit()

        return jsonify(message=f"Usuario '{user.first_name}' con ID '{user.id}' fue eliminado correctamente."), 200
    except Exception as e:
        # Handle any other errors that may occur.
        return jsonify(message="Ocurrió un error al intentar eliminar al usuario."), 500

@bp.route('/<string:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    """
    Endpoint PUT http://127.0.0.1:5000/api/users/<string:user_id> to update the data of a user by ID.
    
    Required:
    - user_id       (str)   Unique user id.

    Return:
    - user_data     (dict)  User data.
    """
    try:
        # Search the user by ID.
        user = User.query.filter_by(id=user_id).first()

        # If the user is not found, return a 404 error.
        if not user:
            return jsonify(message="Usuario no encontrado."), 404

        # Update the user's information with the information provided in the application.
        data = request.json
        for key, value in data.items():
            setattr(user, key, value)

        # Validate the updated data using the validation scheme.
        user_schema.load(data)

        # Save changes to the database.
        db.session.commit()

        return jsonify(message="Se actualizo la data del usuario con exito."), 200
    except ValidationError as err:
        # Handle schema validation errors.
        return jsonify({"message": "Error de validación", "errors": err.messages}), 400
    except Exception as e:
        # Handle any other errors that may occur.
        return jsonify(message="Ocurrió un error al intentar actualizar al usuario."), 500
