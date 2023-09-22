from marshmallow import EXCLUDE, Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.vendors.items import Item


class ItemAutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True
        ordered = True
        unknown = EXCLUDE


class ItemGetInputSchema(Schema):
    item_id_list = fields.List(
        fields.Integer(),
        required=True,
        dump_default=[],
        load_default=[],
    )
    category_list = fields.List(
        fields.String(),
        required=True,
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


class ItemPostInputSchema(Schema):
    category = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(allow_none=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class ItemPutInputSchema(Schema):
    item_id = fields.Integer(required=True)
    category = fields.String(allow_none=True)
    name = fields.String(allow_none=True)
    description = fields.String(allow_none=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class ItemDeleteInputSchema(Schema):
    item_id_list = fields.List(
        fields.Integer(),
        required=True,
    )

    class Meta:
        ordered = True
        unknown = EXCLUDE
