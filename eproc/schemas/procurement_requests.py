from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.procurement_requests import ProcurementRequest
from eproc.schemas.references import ReferenceAutoSchema


class ProcurementRequestAutoSchema(SQLAlchemyAutoSchema):
    reference = fields.Nested(ReferenceAutoSchema)

    class Meta:
        model = ProcurementRequest
        load_instance = True
        ordered = True
        unknown = EXCLUDE


class ProcurementRequestGetInputSchema(Schema):
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
