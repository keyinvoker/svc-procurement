import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel, WIBNow
from eproc.helpers.commons import wibnow


class RFQ(BaseModel):
    __tablename__ = "rfqs"

    id = sa.Column(sa.BigInteger(), primary_key=True)
    fcoid = sa.Column(sa.String(10), nullable=False)  # TODO: Foreign Key
    vendor_id = sa.Column(sa.String(100), sa.ForeignKey("vendors.id"), nullable=False)
    procured_by = sa.Column(sa.String(20), sa.ForeignKey("users.id"), nullable=False)
    reference_id = sa.Column(sa.Integer(), sa.ForeignKey("references.id"), nullable=False, default=0, server_default="0")
    transaction_type = sa.Column(sa.String(4), nullable=False)
    document_number = sa.Column(sa.String(20))
    transaction_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    year = sa.Column(sa.Integer(), nullable=False)
    month = sa.Column(sa.Integer(), nullable=False)
    description = sa.Column(sa.String(500), nullable=False)
    app_source = sa.Column(sa.String(20), nullable=False)

    sequence_number = sa.Column(sa.Integer(), nullable=False)
    dref1 = sa.Column(sa.String(100))
    dref2 = sa.Column(sa.String(100))
    dref3 = sa.Column(sa.String(100))
    flag1 = sa.Column(sa.String(15))
    flag2 = sa.Column(sa.String(15))
    temps = sa.Column(sa.String(100))

    vendor = db.relationship(
        "Vendor", backref=backref(__tablename__, uselist=False)
    )
    procurer = db.relationship(
        "User", backref=backref(__tablename__, uselist=False)
    )
    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
