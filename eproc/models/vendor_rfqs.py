import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel, WIBNow
from eproc.helpers.commons import wibnow


class VendorRFQ(BaseModel):
    __tablename__ = "vendor_rfqs"

    id = sa.Column(sa.BigInteger(), primary_key=True)
    vendor_id = sa.Column(sa.String(20), sa.ForeignKey("vendors.id"), nullable=False)
    fcoid = sa.Column(sa.String())  # TODO: Foreign Key
    reference_id = sa.Column(sa.Integer(), sa.ForeignKey("references.id"), nullable=False, default=0, server_default="0")
    document_number = sa.Column(sa.String(20))
    transaction_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    year = sa.Column(sa.Integer(), nullable=False)
    month = sa.Column(sa.Integer(), nullable=False)
    description = sa.Column(sa.String(500))
    app_source = sa.Column(sa.String(20))

    rfqdn = sa.Column("rfqdn", sa.String(20))
    rfqtn = sa.Column("rfqtn", sa.BigInteger())
    pcppn = sa.Column("pcppn", sa.Numeric(18, 2))
    paytm = sa.Column("paytm", sa.String(200))
    paypd = sa.Column("paypd", sa.String(20))
    paynt = sa.Column("paynt", sa.String(200))

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
