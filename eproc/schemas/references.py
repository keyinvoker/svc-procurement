from decimal import Decimal
from marshmallow import EXCLUDE, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.references import Reference


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
