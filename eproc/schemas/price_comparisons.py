from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.price_comparisons import PriceComparison


class PriceComparisonAutoSchema(SQLAlchemyAutoSchema):
    reference_description = fields.String()

    @post_dump
    def parse_data(self, data: dict, **kwargs):
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = float(value)
        return data

    class Meta:
        model = PriceComparison
        load_instance = True
        ordered = True
        unknown = EXCLUDE
        include_fk = True


class PriceComparisonGetInputSchema(Schema):
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
