from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from typing import List

from eproc.models.procurement_requests import ProcurementRequest
from eproc.schemas.companies.branches import BranchAutoSchema
from eproc.schemas.companies.departments import DepartmentAutoSchema
from eproc.schemas.companies.divisions import DivisionAutoSchema
from eproc.schemas.references import ReferenceAutoSchema
from eproc.schemas.users.users import UserAutoSchema


class ProcurementRequestAutoSchema(SQLAlchemyAutoSchema):
    requester = fields.Nested(UserAutoSchema)
    branch = fields.Nested(BranchAutoSchema)
    department = fields.Nested(DepartmentAutoSchema)
    division = fields.Nested(DivisionAutoSchema)
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
