from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.items.item_categories import ItemCategory


class ItemGroupAutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ItemCategory
        ordered = True
        unknown = EXCLUDE
