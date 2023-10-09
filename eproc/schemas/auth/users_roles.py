from marshmallow import EXCLUDE, Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.auth.users_roles import UserRole


class UserRoleSchema(SQLAlchemyAutoSchema):
    user_id = fields.String()
    role_name_list = fields.List(fields.String())

    class Meta:
        ordered = True
        unknown = EXCLUDE


class UserRoleGetInputSchema(Schema):
    user_id = fields.String(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
