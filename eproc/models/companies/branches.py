import sqlalchemy as sa
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc.models.base_model import BaseModel


class Branch(BaseModel):
    __tablename__ = "branches"

    id = sa.Column(sa.String(), primary_key=True)
    description = sa.Column("descr", sa.String(500), nullable=False)
    nttid = sa.Column("nttid", sa.String(10), nullable=False)
    first_address = sa.Column("addl1", sa.String(150))
    second_address = sa.Column("addl2", sa.String(150))
    third_address = sa.Column("addl3", sa.String(150))
    city = sa.Column("ocity", sa.String(100))
    province = sa.Column("provc", sa.String(100))
    country = sa.Column("cntry", sa.String(100))
    phone_number = sa.Column("phone", sa.String(20))
    fax_number = sa.Column("nofax", sa.String(20))
    capsp = sa.Column("capsp", sa.String(10))
    capct = sa.Column("capct", sa.String(10))
    carct = sa.Column("carct", sa.String(10))
    crtct = sa.Column("crtct", sa.String(10))
    # isact = sa.Column("isact", sa.Integer(), default=0)  # TODO: change to boolean (from BIT)
    # is_active = column_property(
    #     case((isact == 1, True), else_=False)
    # )
