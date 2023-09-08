from marshmallow import EXCLUDE, Schema, fields


class LoginInputSchema(Schema):
    email = fields.String()
    password = fields.String()

    class Meta:
        ordered = True
        unknown = EXCLUDE
