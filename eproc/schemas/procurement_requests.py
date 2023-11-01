from marshmallow import EXCLUDE, Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.procurement_requests import ProcurementRequest


class ProcurementRequestAutoSchema(SQLAlchemyAutoSchema):
    branch_name = fields.String()
    directorate_name = fields.String()
    division_name = fields.String()
    department_name = fields.String()
    reference_description = fields.String()
    requester_full_name = fields.String()

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


class ProcurementRequestDetailSchema(SQLAlchemyAutoSchema):
    item_class_name = fields.String()
    item_group_name = fields.String()
    branch_name = fields.String()
    directorate_name = fields.String()
    division_name = fields.String()
    department_name = fields.String()
    reference_description = fields.String()
    preparer_full_name = fields.String()
    requester_full_name = fields.String()
    cost_center_description = fields.String()
    assessment_notes = fields.List(fields.String())
    assessors = fields.List(fields.String())

    class Meta:
        model = ProcurementRequest
        load_instance = True
        include_fk = True
        ordered = True
        unknown = EXCLUDE


class ProcurementRequestDetailGetInputSchema(Schema):
    id = fields.Integer(required=True)

    class Meta:
        ordered = True
        uniknown = EXCLUDE


class ProcurementRequestPostInputSchema(Schema):
    branch_id = fields.String(required=True)
    directorate_id = fields.String(required=True)
    division_id = fields.String(required=True)
    department_id = fields.String(required=True)
    preparer_id = fields.String(required=True)
    requester_id = fields.String(required=True)
    year = fields.Integer(required=True)
    month = fields.Integer(required=True)
    item_class_id = fields.String(required=True)
    item_category_id = fields.String(required=True)
    item_list = fields.List(fields.Dict(), required=True)
    description = fields.String(validate=validate.Length(max=120))

    class Meta:
        ordered = True
        unknown = EXCLUDE
