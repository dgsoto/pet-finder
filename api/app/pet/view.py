from datetime import datetime

from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import current_user, jwt_required
from app.social_network.view import get_social_networks

from app import db
from app.pet.models import Pet, PetPhotos
from app.pet.schemas import pet_schema, pets_schema, pet_photo_schema


bp = Blueprint("pets", __name__)


@bp.route("/", methods=["POST"])
@jwt_required()
def register_pet():
    """
    Endpoint POST http://127.0.0.1:5000/api/pets/ to create a new pet.

    Required:
    - name          (str)   Unique pet name.
    - breed         (str)   Breed of pet.
    - age           (int)   Age of the pet.
    - size          (str)   Size of the pet.
    - description   (str)   Description of the pet.
    - type          (str)   Value is Wanted or Found.
    - date_lost     (time)  Value is datetime in UTF format.
    - location      (str)   Value of the location of pet.

    Return:
    - pet_data      (dict)  Created pet data.
    """
    # Load the data of the request using the schema PetSchema
    pet_schema_ref = pet_schema
    data = request.json
    try:
        validated_data = pet_schema_ref.load(data)
        validated_data.created_by_id = current_user.id

        db.session.add(validated_data)
        db.session.commit()

        # Return the pet object created as part of the response.
        pet_data = pet_schema.dump(validated_data)
        return jsonify(pet_data), 200
    except ValidationError as err:
        # Manage the errors of validation and return a message according specific error.
        return jsonify(err.messages), 400


@bp.route("/", methods=["GET"])
def get_pets():
    """
    Endpoint GET to list the pets with pagination.
    Examples:
    - http://127.0.0.1:5000/api/pets
    - http://127.0.0.1:5000/api/pets?page=1&per_page=10

    Query Parameters:
    - page      (int)   Page number (default 1).
    - per_page  (int)   Number of pets per page (default 10).

    Return:
    - pets_data (list)  List of pets on the specified page.
    """
    try:
        # Pagination parameters.
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))

        # Query to get paged pets.
        pets = Pet.query.paginate(page=page, per_page=per_page)

        # Serialize results.
        pets_data = pets_schema.dump(pets.items)

        # Fetch networks for each pet and add to pets_data
        #for pet_data in pets_data:
        #    pet_id = pet_data["id"]
        #    pet_networks = get_social_networks()
        #    print(pet_networks)
        #    pet_data["networks"] = pet_networks.get("social_networks", [])

        # Build paginated response.
        response = {
            "pets": pets_data,
            "total_pages": pets.pages,
            "total_pets": pets.total,
            "current_page": page,
        }

        return jsonify(response), 200
    except Exception as e:
        # Handle the error and return an appropriate error message.
        return jsonify({"message": "Error al listar mascotas.", "error": str(e)}), 500


@bp.route("/<string:pet_id>", methods=["GET"])
def get_pet_by_id(pet_id):
    """
    Endpoint GET http://127.0.0.1:5000/api/pets/<string:pet_id> to get a pet by ID.

    Required:
    - pet_id       (str)   Unique pet id.

    Return:
    - pet_data     (dict)  Pet data.
    """
    # Find the pet by ID
    try:
        # Query to search an pet by id in the database.
        pet = Pet.query.filter_by(id=pet_id).first()

        # If the pet is not found, return a 404 Not Found.
        if not pet:
            return jsonify(message="Mascota no encontrado."), 404

        # Serialize the pet and return it as a response.
        pet_data = pet_schema.dump(pet)
        return jsonify(pet_data), 200
    except ValueError:
        raise BadRequest("ID de mascota inválido")
    except ValidationError as err:
        # Handle schema validation errors.
        return jsonify(err.messages), 400


@bp.route("/<string:pet_id>", methods=["DELETE"])
@jwt_required()
def delete_pet_by_id(pet_id):
    """
    Endpoint DELETE http://127.0.0.1:5000/api/pets/<string:pet_id> to delete a pet by ID.

    Required:
    - pet_id       (str)   Unique pet id.

    Return:
    - message      (str)   Success or error message.
    """
    try:
        # Search the pet by ID.
        pet = Pet.query.filter_by(id=pet_id).first()

        # If the pet is not found, return a 404 error.
        if not pet:
            return jsonify(message="Mascota no encontrada."), 404

        if current_user.id != pet.created_by_id:
            return jsonify(message="No tienes permiso para acceder a esta mascota."), 403 # Forbidden

        # Delete the pet from the database.
        db.session.delete(pet)
        db.session.commit()

        return (
            jsonify(
                message=f"Mascota '{pet.name}' con ID '{pet.id}' fue eliminada correctamente."
            ),
            200,
        )
    except Exception as e:
        # Handle any other errors that may occur.
        return jsonify(message="Ocurrió un error al intentar eliminar la mascota."), 500


@bp.route("/<string:pet_id>", methods=["PUT"])
@jwt_required()
def update_pet_by_id(pet_id):
    """
    Endpoint PUT http://127.0.0.1:5000/api/pets/<string:pet_id> to update the data of a pet by ID.

    Required:
    - pet_id       (str)   Unique pet id.

    Return:
    - pet_data     (dict)  Pet data.
    """
    try:
        # Search the pet by ID.
        pet = Pet.query.filter_by(id=pet_id).first()

        # If the pet is not found, return a 404 error.
        if not pet:
            return jsonify(message="Mascota no encontrada."), 404

        if current_user.id != pet.created_by_id:
            return jsonify(message="No tienes permiso para acceder a esta mascota."), 403 # Forbidden

        # Update the pet's information with the information provided in the application.
        data = request.json
        for key, value in data.items():
            setattr(pet, key, value)

        # Validate the updated data using the validation scheme.
        pet_schema.load(data)

        # Save changes to the database.
        db.session.commit()

        return jsonify(message="Se actualizo la data de la mascota con exito."), 200
    except ValidationError as err:
        # Handle schema validation errors.
        return jsonify({"message": "Error de validación", "errors": err.messages}), 400
    except Exception as e:
        # Handle any other errors that may occur.
        return (
            jsonify(message="Ocurrió un error al intentar actualizar la mascota."),
            500,
        )


@bp.route("/<string:pet_id>/photo", methods=["POST"])
@jwt_required()
def upload_pet_image_by_id(pet_id):
    """
    Endpoint POST http://127.0.0.1:5000/api/pets/<string:pet_id>/photo to upload photo for a pet by ID.

    Required:
    - pet_id       (str)   Unique pet id.
    - photo_url    (str)   Url image of the pet.

    Return:
    - pet_data     (dict)  Pet data.
    """
    try:
        photo_url = request.json.get("photo_url")

        # Check if the pet exists
        pet = Pet.query.filter_by(id=pet_id).first()
        if not pet:
            return jsonify(message="Mascota no encontrada."), 404

        if current_user.id != pet.created_by_id:
            return jsonify(message="No tienes permiso para acceder a esta mascota."), 403 # Forbidden

        # Create a PetPhotos instance with the image URL and pet ID
        pet_photo = PetPhotos(pet_id=pet_id, photo_url=photo_url)

        # Add the PetPhotos instance to the database
        db.session.add(pet_photo)
        db.session.commit()

        # Return the pet data with the new image as a response
        pet_data = pet_photo_schema.dump(pet_photo)
        return jsonify(pet_data), 200
    except Exception as e:
        # Handle any other errors that may occur
        return (
            jsonify(
                message="Ocurrió un error al intentar cargar la imagen.", error=str(e)
            ),
            500,
        )
