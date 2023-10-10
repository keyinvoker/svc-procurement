from marshmallow import EXCLUDE, Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class UserRolesSchema(SQLAlchemyAutoSchema):
    user_id = fields.String()
    is_registered = fields.Boolean()
    role_name_list = fields.List(fields.String())

    class Meta:
        ordered = True
        unknown = EXCLUDE


class UserRoleGetInputSchema(Schema):
    user_id = fields.String(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
