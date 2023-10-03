import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class PriceComparison(BaseModel):
    __tablename__ = "price_comparisons"

    id = sa.Column("trnno", sa.String(), primary_key=True)
    rfq_id = sa.Column("rfqtn", sa.Integer(), sa.ForeignKey("rfqs.id"), nullable=False)
    flag1 = sa.Column(sa.String(15))
    flag2 = sa.Column(sa.String(15))
    sqenc = sa.Column("sqenc", sa.Integer(), nullable=False)
    document_number = sa.Column("docno", sa.String(20))
    transaction_date = sa.Column("trndt", sa.DateTime(), nullable=False)
    transaction_type = sa.Column("trnty", sa.String(4), nullable=False)
    year = sa.Column("fisyr", sa.Integer(), nullable=False)
    month = sa.Column("fismn", sa.Integer(), nullable=False)
    description = sa.Column("descr", sa.String(500))
    reference_id = sa.Column("stats", sa.Integer(), sa.ForeignKey("references.id"))
    appsc = sa.Column("appsc", sa.String(20))
    dref1 = sa.Column("dref1", sa.String(100))
    dref2 = sa.Column("dref2", sa.String(100))
    dref3 = sa.Column("dref3", sa.String(100))
    temps = sa.Column("temps", sa.String(100))

    prtno = sa.Column("prtno", sa.Integer())
    recom = sa.Column("recom", sa.String(1000))
    plfon = sa.Column("plfon", sa.Integer())

    rfq = db.relationship(
        "RFQ", backref=backref(__tablename__, uselist=False)
    )
    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
