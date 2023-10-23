from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from typing import List

from eproc.models.procurement_requests import ProcurementRequest
from eproc.schemas.companies.branches import BranchAutoSchema
from eproc.schemas.companies.departments import DepartmentAutoSchema
from eproc.schemas.companies.divisions import DivisionAutoSchema
from eproc.schemas.references import ReferenceAutoSchema
from eproc.schemas.users.employees import EmployeeAutoSchema
from eproc.schemas.users.users import UserAutoSchema
from eproc.schemas.items.item_classes import ItemClassAutoSchema
from eproc.schemas.items.item_groups import ItemGroupAutoSchema


class ProcurementRequestAutoSchema(SQLAlchemyAutoSchema):
    item_class = fields.Nested(ItemClassAutoSchema)
    item_group = fields.Nested(ItemGroupAutoSchema)
    preparer = fields.Nested(UserAutoSchema)
    requester = fields.Nested(EmployeeAutoSchema)
    branch = fields.Nested(BranchAutoSchema)
    department = fields.Nested(DepartmentAutoSchema)
    division = fields.Nested(DivisionAutoSchema)
    reference = fields.Nested(ReferenceAutoSchema)

    requester_full_name = fields.String()
    branch_name = fields.String()
    department_name = fields.String()
    division_name = fields.String()
    reference_description = fields.String()

    @post_dump
    def parse_data(self, data: dict, **kwargs):
        data["item_class_name"] = None
        if data.get("item_class"):
            data["item_class_name"] = data["item_class"]["description"]
        del data["item_class"]

        data["item_group_name"] = None
        if data.get("item_group"):
            data["item_group_name"] = data["item_group"]["description"]
        del data["item_group"]

        data["preparer_full_name"] = None
        if data.get("preparer"):
            data["preparer_full_name"] = data["preparer"]["full_name"]
        del data["preparer"]

        data["requester_full_name"] = None
        if data.get("requester"):
            data["requester_full_name"] = data["requester"]["full_name"]
        del data["requester"]

        for key in ["branch", "department", "division"]:
            data[f"{key}_name"] = None
            if data.get(key):
                data[f"{key}_name"] = data[key]["description"]
            del data[key]

        data["reference_description"] = None
        if data.get("reference"):
            data["reference_description"] = data["reference"]["description"]
        del data["reference"]

        return data

    class Meta:
        model = ProcurementRequest
        load_instance = True
        include_fk = True
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


class ProcurementRequestDetailGetInputSchema(Schema):
    id = fields.Integer(required=True)

    class Meta:
        ordered = True
        uniknown = EXCLUDE
