import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class PurchaseOrder(BaseModel):
    __tablename__ = "purchase_orders"

    id = sa.Column(sa.String(), primary_key=True)
    flag1 = sa.Column(sa.String(15))
    flag2 = sa.Column(sa.String(15))
    transaction_type = sa.Column("trnty", sa.String(4))
    transaction_date = sa.Column("trndt", sa.DateTime(), nullable=False)
    sqenc = sa.Column("sqenc", sa.Integer(), nullable=False)
    document_number = sa.Column("docno", sa.String(20))
    description = sa.Column("descr", sa.String(500), nullable=False)
    purchase_order_type = sa.Column("potyp", sa.String(2))
    prtno = sa.Column("prtno", sa.BigInteger(), nullable=False)
    vendor_id = sa.Column("vdrid", sa.String(), sa.ForeignKey("vendors.id"), nullable=False)
    fcoid = sa.Column(sa.String())  # TODO: Foreign Key
    currency = sa.Column("curcd", sa.String(), nullable=False)
    discn = sa.Column("discn", sa.Numeric(18, 2), nullable=False)
    pcppn = sa.Column("pcppn", sa.Numeric(18, 2), nullable=False)
    paypd = sa.Column("paypd", sa.String(20), nullable=False)
    paytm = sa.Column("paytm", sa.String(200), nullable=False)
    paypd = sa.Column("paypd", sa.String(20), nullable=False)
    paynt = sa.Column("paynt", sa.String(200), nullable=False)
    reference_id = sa.Column("stats", sa.Integer(), sa.ForeignKey("references.id"), nullable=False, default=0)
    appsc = sa.Column("appsc", sa.String(20), nullable=False)
    dref1 = sa.Column("dref1", sa.String(100))
    dref2 = sa.Column("dref2", sa.String(100))
    dref3 = sa.Column("dref3", sa.String(100))
    temps = sa.Column("temps", sa.String(100))

    vendor = db.relationship(
        "Vendor", backref=backref(__tablename__, uselist=False)
    )
    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )