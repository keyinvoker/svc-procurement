import sqlalchemy as sa
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import BaseModel


class Reference(BaseModel):
    __tablename__ = "references"

    reference_id = sa.Column("refid", sa.String())  # TODO: Foreign Key to what table?
    cdnum = sa.Column("cdnum", sa.Integer(), primary_key=True)  # TODO: Foreign Key to what table?
    cdval = sa.Column("cdval", sa.Numeric())
    cdtxt = sa.Column("cdtxt", sa.String())
    description = sa.Column("descr", sa.String(1000))
    zordr = sa.Column("zordr", sa.Integer())
    rsign = sa.Column("rsign", sa.String(), nullable=True)
    dref1 = sa.Column("dref1", sa.String())
    dref2 = sa.Column("dref2", sa.String())
    dref3 = sa.Column("dref3", sa.String())

    isact = sa.Column("isact", sa.Integer(), default=0)  # TODO: change to boolean
    is_active = column_property(
        case((isact == 1, True), else_=False)
    )
