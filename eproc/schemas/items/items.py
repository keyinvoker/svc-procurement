from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.items.items import Item
from eproc.models.items.item_categories import ItemCategory
from eproc.models.items.item_classes import ItemClass


class ItemAutoSchema(SQLAlchemyAutoSchema):
    @post_dump
    def parse_data(self, data: dict, **kwargs):
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = float(value)
        return data

    class Meta:
        model = Item
        ordered = True
        unknown = EXCLUDE


class ItemGetInputSchema(Schema):
    id_list = fields.List(
        fields.Integer(),
        dump_default=[],
        load_default=[],
    )
    item_category_id = fields.String()
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


class ItemClassAutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ItemClass
        load_instance = True
        ordered = True
        unknown = EXCLUDE


class ItemCategoryAutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ItemCategory
        load_instance = True
        ordered = True
        unknown = EXCLUDE


class ItemCategoryGetInputSchema(Schema):
    item_class_id = fields.String(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
