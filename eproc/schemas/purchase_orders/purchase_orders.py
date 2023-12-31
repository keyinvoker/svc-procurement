from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.purchase_orders.purchase_orders import PurchaseOrder
from eproc.models.purchase_orders.purchase_order_items import PurchaseOrderItem


class PurchaseOrderAutoSchema(SQLAlchemyAutoSchema):
    branch_id = fields.String()
    branch_location = fields.String()
    branch_address = fields.String()
    vendor_name = fields.String()
    vendor_address = fields.String()
    reference_description = fields.String()

    @post_dump
    def parse_data(self, data: dict, **kwargs):
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = float(value)
        return data

    class Meta:
        model = PurchaseOrder
        load_instance = True
        ordered = True
        unknown = EXCLUDE
        include_fk = True


class PurchaseOrderGetInputSchema(Schema):
    id_list = fields.List(
        fields.Integer(),
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


class PurchaseOrderDetailGetInputSchema(Schema):
    id = fields.Integer(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class PurchaseOrderItemGetInputSchema(Schema):
    purchase_order_id = fields.Integer(required=True)
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


class PurchaseOrderItemAutoSchema(SQLAlchemyAutoSchema):
    item_name = fields.String()
    unit_of_measurement = fields.String()
    total_amount = fields.Float()
    total_discount_amount = fields.Float()
    total_net_price = fields.Float()
    total_tax_amount = fields.Float()
    total_net_amount = fields.Float()

    @post_dump
    def parse_data(self, data: dict, **kwargs):
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = float(value)
        return data

    class Meta:
        model = PurchaseOrderItem
        ordered = True
        unknown = EXCLUDE
        include_fk = True
