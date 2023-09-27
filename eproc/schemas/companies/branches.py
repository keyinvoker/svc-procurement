from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.companies.branches import Branch


class BranchAutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Branch
        load_instance = True
        ordered = True
        unknown = EXCLUDE
