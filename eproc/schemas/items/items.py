from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.items.items import Item


class ItemAutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        ordered = True
        unknown = EXCLUDE
