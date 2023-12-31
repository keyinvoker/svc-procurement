import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.helpers.commons import wibnow
from eproc.models.base_model import BaseModel, WIBNow


class PurchaseOrderItem(BaseModel):
    __tablename__ = "purchase_order_items"

    line_number = sa.Column(sa.Integer(), nullable=False, primary_key=True, autoincrement=True)
    purchase_order_id = sa.Column(sa.BigInteger(), sa.ForeignKey("purchase_orders.id"), nullable=False, primary_key=True)
    item_id = sa.Column(sa.String(20), sa.ForeignKey("items.id"), nullable=False)
    item_quantity = sa.Column(sa.Numeric(18, 2), default=0.00, server_default="0.00")
    price = sa.Column(sa.Numeric(38, 2), default=0.00, server_default="0.00")
    amount = sa.Column(sa.Numeric(38, 2), default=0.00, server_default="0.00")
    discount_amount = sa.Column(sa.Numeric(38, 2), default=0.00, server_default="0.00")
    tax_amount = sa.Column(sa.Numeric(38, 2), default=0.00, server_default="0.00")
    net_amount = sa.Column(sa.Numeric(38, 2), default=0.00, server_default="0.00")
    net_price = sa.Column(sa.Numeric(38, 2), default=0.00, server_default="0.00")
    required_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )

    lnrf1 = sa.Column(sa.String(200))
    lnrf2 = sa.Column(sa.String(200))
    lnrf3 = sa.Column(sa.String(200))
    lnri1 = sa.Column(sa.BigInteger())
    lnri2 = sa.Column(sa.BigInteger())
    lnri3 = sa.Column(sa.BigInteger())
    lnrd1 = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    lnrd2 = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    lnrd3 = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )

    purchase_order = db.relationship(
        "PurchaseOrder", backref=backref(__tablename__, uselist=False)
    )
    item = db.relationship(
        "Item", backref=backref(__tablename__, uselist=False)
    )
