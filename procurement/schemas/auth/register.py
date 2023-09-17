from marshmallow import EXCLUDE, Schema, fields


class RegisterInputSchema(Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    employee_identification_number = fields.String(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
