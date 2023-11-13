from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.invoices import Invoice


class InvoiceAutoSchema(SQLAlchemyAutoSchema):
    vendor_name = fields.String()
    cost_center_description = fields.String()
    reference_description = fields.String()

    @post_dump
    def parse_data(self, data: dict, **kwargs):
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = float(value)
        return data

    class Meta:
        model = Invoice
        load_instance = True
        ordered = True
        unknown = EXCLUDE
        include_fk = True


class InvoiceSchema(InvoiceAutoSchema):
    class Meta:
        exclude = ["image_path"]


class InvoiceGetInputSchema(Schema):
    id_list = fields.List(
        fields.Integer(),
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


class InvoicePostInputSchema(Schema):
    purchase_order_id = fields.Integer(required=True)
    invoice_number = fields.String(required=True)
    invoice_date = fields.String(required=True)
    invoice_image = fields.Raw(required=True)
    description = fields.String()

    class Meta:
        ordered = True
        unknown = EXCLUDE
