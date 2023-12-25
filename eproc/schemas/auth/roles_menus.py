from marshmallow import EXCLUDE, Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.auth.roles_menus import RoleMenu


class RoleMenuGetInputSchema(Schema):
    role_id_list = fields.List(
        fields.String(),
        dump_default=[],
        load_default=[],
    )
    menu_id_list = fields.List(
        fields.String(),
        dump_default=[],
        load_default=[],
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


class RoleMenuSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RoleMenu
        include_fk = True
        ordered = True
        unknown = EXCLUDE
