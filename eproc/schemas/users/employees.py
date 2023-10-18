from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.users.employees import Employee
from eproc.schemas.companies.branches import BranchAutoSchema
from eproc.schemas.companies.departments import DepartmentAutoSchema
from eproc.schemas.companies.divisions import DivisionAutoSchema
from eproc.schemas.references import ReferenceAutoSchema
from eproc.schemas.users.users import UserAutoSchema


class EmployeeAutoSchema(SQLAlchemyAutoSchema):
    # branch = fields.Nested(BranchAutoSchema)
    # department = fields.Nested(DepartmentAutoSchema)
    # division = fields.Nested(DivisionAutoSchema)
    first_approver_full_name = fields.String()

    class Meta:
        model = Employee
        load_instance = True
        ordered = True
        unknown = EXCLUDE


class EmployeeGetInputSchema(Schema):
    id_list = fields.List(
        fields.Integer(),
        dump_default=[],
        load_default=[],
    )
    entity_id = fields.String(allow_none=True)
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


class EmployeeDetailGetInputSchema(Schema):
    id = fields.String(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class EmployeeDetailSchema(EmployeeAutoSchema):
    branch_name = fields.String()
    directorate_name = fields.String()
    division_name = fields.String()
    department_name = fields.String()
    first_approver_id = fields.String()
    first_approver_full_name = fields.String()
    first_approver_is_active = fields.Boolean()
    second_approver_id = fields.String()
    second_approver_full_name = fields.String()
    second_approver_is_active = fields.Boolean()
    third_approver_id = fields.String()
    third_approver_full_name = fields.String()
    third_approver_is_active = fields.Boolean()
    is_registered = fields.Boolean()

    class Meta:
        ordered = True
        unknown = EXCLUDE
