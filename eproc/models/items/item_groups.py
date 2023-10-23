import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class ItemGroup(BaseModel):
    __tablename__ = "item_groups"

    id = sa.Column(sa.String(10), primary_key=True)
    item_class_id = sa.Column(sa.String(10), sa.ForeignKey("item_classes.id"), nullable=False)
    cost_center_id = sa.Column(sa.String(20), sa.ForeignKey("cost_centers.id"))
    description = sa.Column(sa.String(100), nullable=False)
    fanfa = sa.Column("fanfa", sa.String(5), nullable=False)
    pcsfl = sa.Column("pcsfl", sa.String(10), nullable=False)
    pcsun = sa.Column("pcsun", sa.String(30), nullable=False)
    pcsby = sa.Column("pcsby", sa.String(30), nullable=False)
    apvl1 = sa.Column("apvl1", sa.String(20), nullable=False)
    apvl2 = sa.Column("apvl2", sa.String(20), nullable=False)
    pcsem = sa.Column("pcsem", sa.String(50), nullable=False)
    coadp = sa.Column("coadp", sa.String(20))
    coatr = sa.Column("coatr", sa.String(20))
    slavl = sa.Column("slavl", sa.Boolean(), nullable=False, default=False, server_default="false")
    is_active = sa.Column(sa.Boolean(), nullable=False, default=True, server_default="true")

    item_class = db.relationship(
        "ItemClass", backref=backref(__tablename__, uselist=False)
    )
    cost_center = db.relationship(
        "CostCenter", backref=backref(__tablename__, uselist=False)
    )
