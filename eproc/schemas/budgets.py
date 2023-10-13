from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.budgets import Budget
from eproc.schemas.cost_centers import CostCenterAutoSchema


class BudgetAutoSchema(SQLAlchemyAutoSchema):
    cost_center = fields.Nested(CostCenterAutoSchema)

    @post_dump
    def parse_data(self, data: dict, **kwargs):
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = float(value)
        return data

    class Meta:
        model = Budget
        load_instance = True
        ordered = True
        unknown = EXCLUDE
        include_fk = True


class BudgetGetInputSchema(Schema):
    cost_center_id = fields.String(allow_none=True)
    year = fields.Integer(allow_none=True)
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


class BudgetFileUploadInputSchema(Schema):
    user_id = fields.String(required=True)
    file = fields.Raw(type="file", required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
