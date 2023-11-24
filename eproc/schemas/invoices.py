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


class InvoiceDetailSchema(InvoiceAutoSchema):
    purchase_order_document_number = fields.String()
    # purchase_order_net_amount = fields.Float()  # TODO: ini dapat darimana hitungannya?!
    purchase_order_vendor_id = fields.String()
    purchase_order_vendor_name = fields.String()
    purchase_order_document_number = fields.String()
    cost_center_description = fields.String()
    reference_description = fields.String()

    class Meta:
        ordered = True
        unknown = EXCLUDE
        include_fk = True


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
    year = fields.Integer(required=True)
    month = fields.Integer(required=True)
    termin = fields.Integer(required=True)
    invoice_date = fields.String(required=True)
    invoice_number = fields.String(required=True)
    invoice_amount = fields.Float(required=True)
    description = fields.String()
    tax_percentage = fields.Integer()

    class Meta:
        ordered = True
        unknown = EXCLUDE


class InvoicePutInputSchema(Schema):
    id = fields.Integer(required=True)
    invoice_date = fields.String()
    invoice_number = fields.String()
    invoice_amount = fields.Float()
    description = fields.String()

    class Meta:
        ordered = True
        unknown = EXCLUDE


class InvoiceDetailGetInputSchema(Schema):
    id = fields.Integer(required=True)

    class Meta:
        unknown = EXCLUDE
