import datetime
import enum
from sqlalchemy.orm import relationship

from app import db


class Base(db.Model):
    """Base model that provides some common features, such as automatic 'created'
    and 'modified' date columns.
    """

    __abstract__ = True
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(),
                           onupdate=datetime.datetime.now, nullable=False)


class UserRole(Base):
    """A class representing the different user roles that a user can have in the system.
    """

    def __init__(self, name):
        self.name = name
    
    __tablename__ = 'user_role'
    user_role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)


class AuthUser(Base):
    """A class representing a user that can be authenticated to the system.
    """

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
    
    auth_user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(63), nullable=False)
    last_name = db.Column(db.String(63), nullable=False)
    email = db.Column(db.String(127), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class HasUserRole(Base):
    """A class representing the relationship of a user having been assigned a role.
    """

    def __init__(self, auth_user_id, user_role_id):
        self.auth_user_id = auth_user_id
        self.user_role_id = user_role_id

    __tablename__ = 'has_user_role'

    has_user_role_id = db.Column(db.Integer, primary_key=True)
    auth_user_id = db.Column(db.ForeignKey('auth_user.auth_user_id'), nullable=False, index=True)
    user_role_id = db.Column(db.ForeignKey('user_role.user_role_id'), nullable=False, index=True)

    auth_user = relationship('AuthUser')
    user_role = relationship('UserRole')