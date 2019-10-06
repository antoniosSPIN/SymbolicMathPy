from marshmallow import Schema, fields
from marshmallow.validate import Length


class LoginSchema(Schema):
    token = fields.Integer(strict=True, required=True, validate=Length(min=128, max=128))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=Length(min=8))
