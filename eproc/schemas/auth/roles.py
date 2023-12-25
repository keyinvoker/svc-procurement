from marshmallow import EXCLUDE, Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.auth.roles import Role


class RoleAutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True
        ordered = True
        unknown = EXCLUDE


class RoleGetInputSchema(Schema):
    id_list = fields.List(
        fields.String(),
        dump_default=[],
        load_default=[],
    )
    search_query = fields.String(
        allow_none=True,
        dump_default="",
        load_default="",
    )
    limit = fields.Integer(
        allow_none=True,
        dump_default=None,
        load_default=None,
    )
    offset = fields.Integer(
        allow_none=True,
        dump_default=0,
        load_default=0,
    )

    class Meta:
        ordered = True
        unknown = EXCLUDE
