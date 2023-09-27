from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.companies.divisions import Division


class DivisionAutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Division
        load_instance = True
        ordered = True
        unknown = EXCLUDE
