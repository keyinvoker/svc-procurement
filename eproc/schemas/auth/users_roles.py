from marshmallow import EXCLUDE, Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class UserRoleSchema(SQLAlchemyAutoSchema):
    user_id = fields.String()
    user_full_name = fields.String()
    role_id_list = fields.List(fields.String())
    role_name_list = fields.List(fields.String())

    class Meta:
        ordered = True
        unknown = EXCLUDE


class UserRoleGetInputSchema(Schema):
    user_id = fields.String()

    class Meta:
        ordered = True
        unknown = EXCLUDE


class UserRolePutInputSchema(Schema):
    user_id = fields.String(required=True)
    role_id_list = fields.List(fields.String(), required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
