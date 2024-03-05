# Archivo solo de ejemplo para un schema del modelo user
from marshmallow import fields, validate
from app import ma
from app.pet.models import Pet, PetPhotos, SocialProfile


# User Schemas
class PetSchema(ma.SQLAlchemyAutoSchema):

    id = fields.String(dump_only=True) # Este campo se usa solo para volcar datos
    name = fields.String(required=True)
    breed = fields.String()
    age = fields.Integer()
    size = fields.String()
    description = fields.String()
    status = fields.String(validate=validate.OneOf(['Found', 'Lost']), default='Found')
    type = fields.String(validate=validate.OneOf(['Found', 'Wanted']))
    date_lost = fields.DateTime()
    date_found = fields.DateTime()
    created_by_id = fields.String()
    image_url = fields.String()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    location = fields.String()
    revised = fields.Boolean()
    
    class Meta:
        model = Pet
        fields = ['id', 'name', 'breed', 'age', 'size', 'description', 'status', 'type', 'date_lost', 'date_found', 'created_by_id', 'image_url', 'created_at', 'updated_at', 'location', 'revised']
        load_instance = True

pet_schema = PetSchema()
pets_schema = PetSchema(many=True)


class PetPhotosSchema(ma.SQLAlchemyAutoSchema):

    id = fields.String(dump_only=True) # Este campo se usa solo para volcar datos
    pet_id = fields.String()
    photo_url = fields.String()

    class Meta:
        model = PetPhotos
        fields = ['id', 'pet_id', 'photo_url']
        load_instance = True

pet_photo_schema = PetPhotosSchema()
pets_photos_schema = PetPhotosSchema(many=True)


class SocialProfileSchema(ma.SQLAlchemyAutoSchema):

    id = fields.String(dump_only=True) # Este campo se usa solo para volcar datos
    pet_id = fields.String()
    social_media = fields.String(validate=validate.OneOf(['Facebook', 'Twitter', 'Instagram', 'LinkedIn']), default='Facebook')
    profile_url = fields.String()

    class Meta:
        model = SocialProfile
        fields = ['id', 'pet_id', 'social_media', 'profile_url']
        load_instance = True

social_network_schema = SocialProfileSchema()
social_networks_schema = SocialProfileSchema(many=True)
