import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel, WIBNow
from eproc.helpers.commons import wibnow


class PriceComparison(BaseModel):
    __tablename__ = "price_comparisons"

    id = sa.Column(sa.BigInteger(), primary_key=True)
    rfq_id = sa.Column(sa.Integer(), sa.ForeignKey("rfqs.id"), nullable=False)
    reference_id = sa.Column(sa.Integer(), sa.ForeignKey("references.id"), nullable=False, default=0, server_default="0")
    document_number = sa.Column(sa.String(20))
    transaction_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    transaction_type = sa.Column(sa.String(4), nullable=False)
    year = sa.Column(sa.Integer(), nullable=False)
    month = sa.Column(sa.Integer(), nullable=False)
    description = sa.Column(sa.String(500))
    app_source = sa.Column(sa.String(20))

    prtno = sa.Column("prtno", sa.Integer())
    recom = sa.Column("recom", sa.String(1000))
    plfon = sa.Column("plfon", sa.Integer())

    sqenc = sa.Column("sqenc", sa.Integer(), nullable=False)
    flag1 = sa.Column(sa.String(15))
    flag2 = sa.Column(sa.String(15))
    dref1 = sa.Column(sa.String(100))
    dref2 = sa.Column(sa.String(100))
    dref3 = sa.Column(sa.String(100))
    temps = sa.Column("temps", sa.String(100))

    rfq = db.relationship(
        "RFQ", backref=backref(__tablename__, uselist=False)
    )
    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
