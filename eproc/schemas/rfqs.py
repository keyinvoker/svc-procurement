from marshmallow import EXCLUDE, Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from typing import List

from eproc.models.enums import TransactionType
from eproc.models.rfqs.rfqs import RFQ

TRANSACTION_TYPES: List[str] = TransactionType._member_names_


class RFQAutoSchema(SQLAlchemyAutoSchema):
    vendor_name = fields.String()
    branch_first_address = fields.String()
    branch_second_address = fields.String()
    reference_description = fields.String()
    procurer_id = fields.String()
    procurer_full_name = fields.String()

    class Meta:
        model = RFQ
        load_instance = True
        ordered = True
        unknown = EXCLUDE
        include_fk = True


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


class RFQPostInputSchema(Schema):
    branch_id = fields.String(required=True)
    year = fields.Integer(required=True)
    month = fields.Integer(required=True)
    vendor_id_list = fields.List(fields.String(), required=True)
    purchase_request_id_list = fields.List(fields.Integer(), required=True)
    description = fields.String(
        validate=validate.Length(max=500),
        required=True,
    )
    transaction_type = fields.String(
        validate=validate.OneOf(TRANSACTION_TYPES),
        required=True,
    )

    class Meta:
        ordered = True
        unknown = EXCLUDE


class RFQDetailGetInputSchema(Schema):
    id = fields.Integer(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
