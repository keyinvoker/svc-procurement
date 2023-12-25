from marshmallow import EXCLUDE, Schema, fields


class LoginInputSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
