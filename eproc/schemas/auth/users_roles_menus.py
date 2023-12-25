from marshmallow import EXCLUDE, Schema, fields


class UserRoleMenuSchema(Schema):
    user_id = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE
        ordered = True
