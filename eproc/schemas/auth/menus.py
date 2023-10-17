from marshmallow import EXCLUDE, Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.auth.menus import Menu


class MenuSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Menu
        load_instance = True
        ordered = True
        unknown = EXCLUDE
        include_fk = True


class MenuGetInputSchema(Schema):
    id_list = fields.List(
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
