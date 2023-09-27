import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class RFQ(BaseModel):
    __tablename__ = "rfqs"

    id = sa.Column("trnno", sa.String(), primary_key=True)
    flag1 = sa.Column(sa.String(15))
    flag2 = sa.Column(sa.String(15))
    transaction_type = sa.Column("trnty", sa.String(4), nullable=False)
    sqenc = sa.Column("sqenc", sa.Integer(), nullable=False)
    document_number = sa.Column("docno", sa.String(20))
    transaction_date = sa.Column("trndt", sa.DateTime(), nullable=False)
    period = sa.Column("fisyr", sa.Integer(), nullable=False)
    fismn = sa.Column("fismn", sa.Integer(), nullable=False)
    vendor_id = sa.Column("vdrid", sa.String(), sa.ForeignKey("vendors.id"), nullable=False)
    fcoid = sa.Column(sa.String())  # TODO: Foreign Key
    description = sa.Column("descr", sa.String(500))
    procured_by = sa.Column("prcby", sa.String(), sa.ForeignKey("users.id"), nullable=False)
    reference_id = sa.Column("stats", sa.Integer(), sa.ForeignKey("references.id"))
    appsc = sa.Column("appsc", sa.String(20))
    dref1 = sa.Column("dref1", sa.String(100))
    dref2 = sa.Column("dref2", sa.String(100))
    dref3 = sa.Column("dref3", sa.String(100))
    temps = sa.Column("temps", sa.String(100))

    vendor = db.relationship(
        "Vendor", backref=backref(__tablename__, uselist=False)
    )
    procurer = db.relationship(
        "User", backref=backref(__tablename__, uselist=False)
    )
    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
