import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class Budget(BaseModel):
    __tablename__ = "budgets"


    cost_center_id = sa.Column(sa.String(20), sa.ForeignKey("cost_centers.id"), primary_key=True)
    year = sa.Column(sa.Integer(), primary_key=True)
    upload_count = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    amount = sa.Column(sa.Numeric(38, 2), nullable=False)

    cost_center = db.relationship(
        "CostCenter", backref=backref(__tablename__, uselist=False)
    )
