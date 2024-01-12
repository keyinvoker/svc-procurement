import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class RFQItem(BaseModel):
    __tablename__ = "rfq_items"

    rfq_id = sa.Column(sa.BigInteger(), sa.ForeignKey("rfqs.id"), nullable=False, primary_key=True)
    line_number = sa.Column(sa.Integer(), nullable=False, primary_key=True, autoincrement=True)
    procurement_request_id = sa.Column(sa.BigInteger(), sa.ForeignKey("procurement_requests.id"), nullable=False)
    item_id = sa.Column(sa.String(20), sa.ForeignKey("items.id"), nullable=False)

    rfq = db.relationship(
        "RFQ", backref=backref(__tablename__, uselist=False)
    )
    procurement_request = db.relationship(
        "ProcurementRequest", backref=backref(__tablename__, uselist=False)
    )
    item = db.relationship(
        "Item", backref=backref(__tablename__, uselist=False)
    )
