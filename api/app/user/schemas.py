# Archivo solo de ejemplo para un schema del modelo user
import copy
import re
from marshmallow import fields, validate, ValidationError
from app import ma
from app.user.models import User, Notification

VALID_EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def no_html_validator(value):
    if '<' in value or '>' in value:
        raise ValidationError('No se permiten etiquetas HTML')

def validate_unique_username(value):
    existing_user = User.query.filter_by(username=value).first()
    if existing_user:
        raise ValidationError(f"El nombre de usuario '{value}' ya está en uso.")

def validate_unique_email(value):
    existing_email = User.query.filter_by(email=value).first()
    if existing_email:
        raise ValidationError(f"El correo electrónico '{value}' ya está en uso.")

def validate_email(email):
    if not re.match(VALID_EMAIL_PATTERN, email):
        raise ValidationError(f"El correo electrónico '{email}' proporcionado no es válido.")


# User Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    id = fields.String(dump_only=True) # Este campo se usa solo para volcar datos
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_active = fields.Bool(dump_only=True)

    validate_field_value = [
        validate.Length(min=3, max=50, error="Length must be between 3 and 50 characters."),
        validate.Regexp(r'^[a-zA-Z]*$', error='El nombre solo puede contener letras'),
        validate.NoneOf([None], error='El nombre no puede ser nulo'),
        no_html_validator,
    ]
    validate_field_value_for_username = copy.deepcopy(validate_field_value)
    validate_field_value_for_username[1] = validate_unique_username

    validate_field_value_for_email = [
        validate.Length(min=1, max=255),
        validate_unique_email,
        validate_email
    ]

    validate_field_value_for_address = [
        validate.Length(min=1, max=255, error="La dirección debe tener entre 1 y 255 caracteres."),
        validate.Regexp(r'^[a-zA-Z0-9]+(?:\s[a-zA-Z0-9]+)*$', error="La dirección solo puede contener caracteres alfanuméricos y no puede empezar ni terminar con un espacio en blanco."),
        no_html_validator
    ]

    validate_field_value_for_password = [
        validate.Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#!])[A-Za-z\d@#!]+$',
                        error="La contraseña debe contener al menos una letra minúscula, una letra mayúscula, un número y un carácter especial (@, #, ! o $).")
    ]

    password = fields.String(load_only=True)
    first_name = fields.String(validate=validate_field_value)
    last_name = fields.String(validate=validate_field_value)
    username = fields.String(validate=validate_field_value_for_username)
    email = fields.Email(validate=validate_field_value_for_email)
    address = fields.String(validate=validate_field_value_for_address)
    avatar_url = fields.String(validate=validate.URL())

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'address', 'password', 'role', 'avatar_url', 'created_at', 'updated_at', 'reputation', 'is_active']
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class NotificationSchema(ma.SQLAlchemyAutoSchema):

    id = fields.String(dump_only=True) # Este campo se usa solo para volcar datos
    user_id = fields.String()
    created_at = fields.DateTime(dump_only=True)
    message = fields.String()

    class Meta:
        model = Notification
        fields = ['id', 'user_id', 'created_at', 'message']
        load_instance = True

notification_schema = NotificationSchema()
notifications_schema = NotificationSchema(many=True)
