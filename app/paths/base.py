from marshmallow import Schema, EXCLUDE


class Base(Schema):
    class Meta():
        unknown = EXCLUDE
