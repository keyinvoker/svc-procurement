from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.rfqs import RFQ
from eproc.schemas.references import ReferenceAutoSchema
from eproc.schemas.users.users import UserAutoSchema
from eproc.schemas.vendors.vendors import VendorAutoSchema


class RFQAutoSchema(SQLAlchemyAutoSchema):
    vendor = fields.Nested(VendorAutoSchema)
    assessor = fields.Nested(UserAutoSchema)
    reference = fields.Nested(ReferenceAutoSchema)

    @post_dump
    def parse_data(self, data: dict, **kwargs):
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = float(value)
        return data

    class Meta:
        model = RFQ
        load_instance = True
        ordered = True
        unknown = EXCLUDE


class RFQGetInputSchema(Schema):
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
