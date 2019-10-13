from marshmallow import fields
from marshmallow.validate import Length
from app.paths.base import Base


class LoginSchema(Base):
    token = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=Length(min=8))
