from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.items.items import Item
from eproc.models.items.item_categories import ItemCategory
from eproc.models.items.item_classes import ItemClass


class ItemAutoSchema(SQLAlchemyAutoSchema):
    item_category_description = fields.String()
    item_class_id = fields.String()
    item_class_description = fields.String()
    cost_center_description = fields.String()
    required_days_interval = fields.Integer()

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
        include_fk = True


class ItemGetInputSchema(Schema):
    id_list = fields.List(
        fields.String(),
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


class ItemPostInputSchema(Schema):
    id = fields.String(required=True)
    description = fields.String(required=True)
    unit_of_measurement = fields.String(required=True)
    cost_center_id = fields.String(required=True)
    minimum_quantity = fields.Float(required=True)
    item_category_id = fields.String(required=True)
    sla = fields.Integer(required=True)
    is_adjustable = fields.Boolean()
    is_active = fields.Boolean()

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
        include_fk = True


class ItemCategoryGetInputSchema(Schema):
    item_class_id = fields.String(
        default=None,
        dump_default=None,
        load_default=None,
    )

    class Meta:
        ordered = True
        unknown = EXCLUDE
