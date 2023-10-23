from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.items.item_groups import ItemGroup


class ItemGroupAutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ItemGroup
        ordered = True
        unknown = EXCLUDE
