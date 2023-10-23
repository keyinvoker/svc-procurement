from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.items.procurement_request_items import ProcurementRequestItem
from eproc.schemas.items.items import ItemAutoSchema


class ProcurementRequestItemAutoSchema(SQLAlchemyAutoSchema):
    item = fields.Nested(ItemAutoSchema)

    @post_dump
    def parse_data(self, data: dict, **kwargs):
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = float(value)
        
        data["item_name"] = None
        if data.get("item"):
            data["item_name"] = data["item"]["description"]
        del data["item"]

        return data

    class Meta:
        model = ProcurementRequestItem
        include_fk = True
        ordered = True
        unknown = EXCLUDE


class ProcurementRequesItemGetInputSchema(Schema):
    procurement_request_id = fields.Integer(required=True)
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
