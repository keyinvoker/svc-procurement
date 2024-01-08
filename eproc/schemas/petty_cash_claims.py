from marshmallow import EXCLUDE, Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.petty_cash_claims import PettyCashClaim


class PettyCashClaimSchema(SQLAlchemyAutoSchema):
    item_class_name = fields.String()
    item_category_name = fields.String()
    branch_name = fields.String()
    cost_center_description = fields.String()
    reference_description = fields.String()
    preparer_full_name = fields.String()
    requester_full_name = fields.String()

    class Meta:
        model = PettyCashClaim
        load_instance = True
        ordered = True
        unknown = EXCLUDE
        include_fk = True


class PettyCashClaimGetInputSchema(Schema):
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