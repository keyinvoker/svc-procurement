from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.enums import SystemConfigOption
from eproc.models.references import Reference

SYSTEM_CONFIG_OPTIONS = [
    option.name for option in SystemConfigOption
]


class ReferenceAutoSchema(SQLAlchemyAutoSchema):
    @post_dump
    def parse_data(self, data: dict, **kwargs):
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = float(value)
        return data

    class Meta:
        model = Reference
        load_instance = True
        ordered = True
        unknown = EXCLUDE


class SystemConfigGetInputSchema(Schema):
    option = fields.String(
        validate=validate.OneOf(SYSTEM_CONFIG_OPTIONS),
        required=True
    )

    @post_dump
    def parse_data(self, data: dict, **kwargs):
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = float(value)
        return data

    class Meta:
        ordered = True
        unknown = EXCLUDE
