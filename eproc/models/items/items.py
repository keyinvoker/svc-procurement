import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class Item(BaseModel):
    __tablename__ = "items"

    id = sa.Column(sa.String(10), primary_key=True)
    item_category_id = sa.Column(sa.String(10), sa.ForeignKey("item_categories.id"), nullable=False)
    cost_center_id = sa.Column(sa.String(20), sa.ForeignKey("cost_centers.id"))
    description = sa.Column(sa.String(100), nullable=False)
    unit_of_measurement = sa.Column(sa.String(20), nullable=False)
    minimum_quantity = sa.Column(sa.Numeric(18, 2), nullable=False, default=0.0, server_default="0.0")
    slavl = sa.Column("slavl", sa.Integer(), nullable=False)
    isadj = sa.Column("isadj", sa.Boolean(), nullable=False, default=False, server_default="false")
    tags = sa.Column(sa.String(20))
    is_active = sa.Column(sa.Boolean(), nullable=False, default=True, server_default="true")

    item_category = db.relationship(
        "ItemCategory", backref=backref(__tablename__, uselist=False)
    )
    cost_center = db.relationship(
        "CostCenter", backref=backref(__tablename__, uselist=False)
    )
