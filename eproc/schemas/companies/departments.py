from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.companies.departments import Department


class DepartmentAutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Department
        load_instance = True
        ordered = True
        unknown = EXCLUDE
