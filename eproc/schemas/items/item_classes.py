from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.items.item_classes import ItemClass


class ItemClassAutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ItemClass
        ordered = True
        unknown = EXCLUDE
