from flask import Blueprint, jsonify, request
from app import db
from app.user.models import Notification
from app.user.schemas import notification_schema, notifications_schema
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

bp = Blueprint('notifications', __name__)


@bp.route('/', methods=['POST'])
def register_notification():
    """
    Endpoint POST http://127.0.0.1:5000/api/notifications to create a new notification.

    Required:
    - message           (str)   Message for user.
    - user_id           (str)   User id.
    
    Return:
    - notification_data (dict)  Created notification data.
    """
    # Load the data of the request using the schema NotificationSchema
    notification_schema_ref = notification_schema
    data = request.json
    try:
        validated_data = notification_schema_ref.load(data)

        db.session.add(validated_data)
        db.session.commit()
        
        # Return the notification object created as part of the response.
        notification_data = notification_schema.dump(validated_data)
        return jsonify(notification_data), 200
    except ValidationError as err:
        # Manage the errors of validation and return a message according specific error.
        return jsonify(err.messages), 400

@bp.route('/', methods=['GET'])
def get_notifications():
    """
    Endpoint GET to list the notifications with pagination.
    Examples:
    - http://127.0.0.1:5000/api/notifications
    - http://127.0.0.1:5000/api/notifications?page=1&per_page=5

    Query Parameters:
    - page      (int)   Page number (default 1).
    - per_page  (int)   Number of notifications per page (default 5).

    Return:
    - notifications_data (list)  List of notifications on the specified page.
    """
    try:
        # Pagination parameters.
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))

        # Query to get paged notifications.
        notifications = Notification.query.paginate(page=page, per_page=per_page)

        # Serialize results.
        notifications_data = notifications_schema.dump(notifications.items)

        # Build paginated response.
        response = {
            "pets": notifications_data,
            "total_pages": notifications.pages,
            "total_pets": notifications.total,
            "current_page": page
        }

        return jsonify(response), 200
    except Exception as e:
        # Handle the error and return an appropriate error message.
        return jsonify({"message": "Error al listos mensajes.", "error": str(e)}), 500

@bp.route('/<string:notification_id>', methods=['GET'])
def get_notification_by_id(notification_id):
    """
    Endpoint GET http://127.0.0.1:5000/api/notifications/<string:notification_id> to get a notification by ID.
    
    Required:
    - notification_id       (str)   Unique notification id.

    Return:
    - notification_data     (dict)  Notification data.
    """
    # Find the notification by ID
    try:
        # Query to search an notification by id in the database.
        notification = Notification.query.filter_by(id=notification_id).first()

        # If the notification is not found, return a 404 Not Found.
        if not notification:
            return jsonify(message="Mensaje no encontrado."), 404

        # Serialize the notification and return it as a response.
        notification_data = notification_schema.dump(notification)
        return jsonify(notification_data), 200
    except ValueError:
        raise BadRequest("ID de mensaje inválido")
    except ValidationError as err:
        # Handle schema validation errors.
        return jsonify(err.messages), 400

@bp.route('/<string:notification_id>', methods=['DELETE'])
def delete_notification_by_id(notification_id):
    """
    Endpoint DELETE http://127.0.0.1:5000/api/notifications/<string:notification_id> to delete a message by ID.
    
    Required:
    - notification_id       (str)   Unique notification id.

    Return:
    - message      (str)   Success or error message.
    """
    try:
        # Search the message by ID.
        notification = Notification.query.filter_by(id=notification_id).first()

        # If the message is not found, return a 404 error.
        if not notification:
            return jsonify(message="Mensaje no encontrado."), 404

        # Delete the message from the database.
        db.session.delete(notification)
        db.session.commit()

        return jsonify(message=f"Mensaje con ID '{notification.id}' fue eliminada correctamente."), 200
    except Exception as e:
        # Handle any other errors that may occur.
        return jsonify(message="Ocurrió un error al intentar eliminar el mensaje."), 500

@bp.route('/<string:notification_id>', methods=['PUT'])
def update_notification_by_id(notification_id):
    """
    Endpoint PUT http://127.0.0.1:5000/api/notifications/<string:notification_id> to update the data of a message by ID.
    
    Required:
    - notification_id       (str)   Unique notification id.

    Return:
    - notification_data     (dict)  Notification data.
    """
    try:
        # Search the message by ID.
        notification = Notification.query.filter_by(id=notification_id).first()

        # If the message is not found, return a 404 error.
        if not notification:
            return jsonify(message="Mensaje no encontrado."), 404

        # Update the message's information with the information provided in the application.
        data = request.json
        for key, value in data.items():
            setattr(notification, key, value)

        # Validate the updated data using the validation scheme.
        notification_schema.load(data)

        # Save changes to the database.
        db.session.commit()

        return jsonify(message="Se actualizo la data del mensaje con exito."), 200
    except ValidationError as err:
        # Handle schema validation errors.
        return jsonify({"message": "Error de validación", "errors": err.messages}), 400
    except Exception as e:
        # Handle any other errors that may occur.
        return jsonify(message="Ocurrió un error al intentar actualizar el mensaje."), 500
