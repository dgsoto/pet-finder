from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import jwt_required

from app import db
from app.pet.models import SocialProfile
from app.pet.schemas import social_network_schema, social_networks_schema


bp = Blueprint("networks", __name__)


@bp.route("/", methods=["POST"])
@jwt_required()
def register_social_network_for_pet():
    """
    Endpoint POST http://127.0.0.1:5000/api/networks/ to create a new social newtwork.

    Required:
    - pet_id            (str)   Unique pet id.
    - social_media      (str)   Social media type as Facebook, Twitter, Instagram or LinkedIn.
    - profile_url       (str)   URL of social media.

    Return:
    - social_media_data (dict)  Created social media data.
    """
    # Load the data of the request using the schema SocialNetworkSchema
    social_network_schema_ref = social_network_schema
    data = request.json
    try:
        validated_data = social_network_schema_ref.load(data)

        db.session.add(validated_data)
        db.session.commit()

        # Return the social network object created as part of the response.
        social_media_data = social_network_schema.dump(validated_data)
        return jsonify(social_media_data), 200
    except ValidationError as err:
        # Manage the errors of validation and return a message according specific error.
        return jsonify(err.messages), 400


@bp.route("/", methods=["GET"])
def get_social_networks():
    """
    Endpoint GET to list the social networks with pagination and optional filters.
    Examples:
    - http://127.0.0.1:5000/api/networks
    - http://127.0.0.1:5000/api/networks?page=1&per_page=5
    - http://127.0.0.1:5000/api/networks?pet_id=<pet_id>
    - http://127.0.0.1:5000/api/networks?social_media=Facebook

    Query Parameters:
    - page          (int)   Page number (default 1).
    - per_page      (int)   Number of social networks per page (default 5).
    - pet_id        (str)   Filter by pet ID.
    - social_media  (str)   Filter by social media type (e.g., facebook, twitter, instagram).

    Return:
    - networks_data (list)  List of social networks on the specified page that match the filters.
    """
    try:
        # Pagination parameters.
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 5))

        # Filter parameters.
        pet_id = request.args.get("pet_id")
        social_media = request.args.get("social_media")

        # Base query to get paged social networks.
        query = SocialProfile.query

        # Apply filters if provided.
        if pet_id:
            query = query.filter(SocialProfile.pet_id == pet_id)
        if social_media:
            query = query.filter(SocialProfile.social_media == social_media)

        # Execute the query and paginate the results.
        social_networks = query.paginate(page=page, per_page=per_page)

        # Serialize results.
        networks_data = social_networks_schema.dump(social_networks.items)

        # Build paginated response.
        response = {
            "social_networks": networks_data,
            "total_pages": social_networks.pages,
            "total_networks": social_networks.total,
            "current_page": page,
        }

        return jsonify(response), 200
    except Exception as e:
        # Handle the error and return an appropriate error message.
        return jsonify({"message": "Error al listar redes sociales.", "error": str(e)}), 500


@bp.route("/<string:network_id>", methods=["GET"])
def get_social_network_by_id(network_id):
    """
    Endpoint GET http://127.0.0.1:5000/api/networks/<string:network_id> to get a social network by ID.

    Required:
    - network_id            (str)   Unique social network id.

    Return:
    - social_network_data   (dict)  Social Network Data.
    """
    # Find the social network by ID
    try:
        # Query to search an social network by id in the database.
        social_network = SocialProfile.query.filter_by(id=network_id).first()

        # If the social network is not found, return a 404 Not Found.
        if not social_network:
            return jsonify(message="Red social no encontrado."), 404

        # Serialize the social network and return it as a response.
        social_network_data = social_network_schema.dump(social_network)
        return jsonify(social_network_data), 200
    except ValueError:
        raise BadRequest("ID de red social inválido")
    except ValidationError as err:
        # Handle schema validation errors.
        return jsonify(err.messages), 400
