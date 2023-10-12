import sqlalchemy as sa
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import BaseModel


class Reference(BaseModel):
    __tablename__ = "references"

    id = sa.Column(sa.Integer(), primary_key=True)
    refid = sa.Column("refid", sa.String(20), nullable=False)  # TODO: Foreign Key to what table?
    cdval = sa.Column("cdval", sa.Numeric(18, 2), nullable=False)
    cdtxt = sa.Column("cdtxt", sa.String(100))
    description = sa.Column("descr", sa.String(1000), nullable=False)
    zordr = sa.Column("zordr", sa.BigInteger(), nullable=False)
    rsign = sa.Column("rsign", sa.String(12))
    dref1 = sa.Column(sa.String(20))
    dref2 = sa.Column(sa.String(200))
    dref3 = sa.Column(sa.String(20))

    isact = sa.Column("isact", sa.Integer(), default=1)  # TODO: change to boolean
    is_active = column_property(
        case((isact == 1, True), else_=False)
    )
