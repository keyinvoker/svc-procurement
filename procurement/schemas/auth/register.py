from marshmallow import EXCLUDE, Schema, fields


class RegisterInputSchema(Schema):
    name = fields.String()
    email = fields.String()
    password = fields.String()
    employee_identification_number = fields.String()

    class Meta:
        ordered = True
        unknown = EXCLUDE
