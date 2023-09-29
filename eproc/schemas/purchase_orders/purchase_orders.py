from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.purchase_orders.purchase_orders import PurchaseOrder
from eproc.schemas.references import ReferenceAutoSchema
from eproc.schemas.vendors.vendors import VendorAutoSchema


class PurchaseOrderAutoSchema(SQLAlchemyAutoSchema):
    vendor = fields.Nested(VendorAutoSchema)
    reference = fields.Nested(ReferenceAutoSchema)

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
