import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import (
    BaseModel,
    WIBNow,
    wibnow
)


class PurchaseOrder(BaseModel):
    __tablename__ = "purchase_orders"

    id = sa.Column(sa.BigInteger(), primary_key=True)
    fcoid = sa.Column(sa.String(20))  # TODO: Foreign Key
    vendor_id = sa.Column(sa.String(20), sa.ForeignKey("vendors.id"), nullable=False)
    reference_id = sa.Column(sa.Integer(), sa.ForeignKey("references.id"), nullable=False, default=0)
    transaction_type = sa.Column(sa.String(4))
    transaction_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    document_number = sa.Column(sa.String(20))
    purchase_order_type = sa.Column(sa.String(2))
    currency = sa.Column(sa.String(), nullable=False)
    description = sa.Column(sa.String(500), nullable=False)
    app_source = sa.Column(sa.String(20), nullable=False)

    prtno = sa.Column("prtno", sa.BigInteger(), nullable=False)
    discn = sa.Column("discn", sa.Numeric(18, 2), nullable=False)
    pcppn = sa.Column("pcppn", sa.Numeric(18, 2), nullable=False)
    paypd = sa.Column("paypd", sa.String(20), nullable=False)
    paytm = sa.Column("paytm", sa.String(200), nullable=False)
    paypd = sa.Column("paypd", sa.String(20), nullable=False)
    paynt = sa.Column("paynt", sa.String(200), nullable=False)

    sqenc = sa.Column("sqenc", sa.Integer(), nullable=False)
    dref1 = sa.Column(sa.String(100))
    dref2 = sa.Column(sa.String(100))
    dref3 = sa.Column(sa.String(100))
    flag1 = sa.Column(sa.String(15))
    flag2 = sa.Column(sa.String(15))
    temps = sa.Column(sa.String(100))

    vendor = db.relationship(
        "Vendor", backref=backref(__tablename__, uselist=False)
    )
    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
