from app import db
from app.utils import generate_id
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.String(64), primary_key=True, default=generate_id)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Enum('User', 'Administrator', name='role'), default='User')
    avatar_url = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    reputation = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    # Relations
    # ...

class Notification(db.Model):
    __tablename__ = "Notification"

    id = db.Column(db.String(64), primary_key=True, default=generate_id)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    message = db.Column(db.String, nullable=False)

    # Relations of FOREIGN KEY
    user_id = db.Column(db.String, db.ForeignKey('User.id'))
