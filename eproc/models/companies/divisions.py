import sqlalchemy as sa
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import BaseModel


class Division(BaseModel):
    __tablename__ = "divisions"

    id = sa.Column(sa.String(), primary_key=True)
    description = sa.Column("descr", sa.String(500), nullable=False)
    nttid = sa.Column("nttid", sa.String(10), nullable=False)
    # isact = sa.Column("isact", sa.Integer(), default=0)  # TODO: change to boolean (from BIT)
    # is_active = column_property(
    #     case((isact == "1", True), else_=False)
    # )
