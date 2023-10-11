import sqlalchemy as sa
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import BaseModel


class CostCenter(BaseModel):
    __tablename__ = "cost_centers"

    id = sa.Column(sa.String(20), primary_key=True)
    coafc = sa.Column("coafc", sa.String(26))
    coagp = sa.Column("coagp", sa.String(20), nullable=False)
    description = sa.Column(sa.String(300), nullable=False)
    alldb = sa.Column("alldb", sa.Boolean(), nullable=False, default=True, server_default="true")
    allcr = sa.Column("allcr", sa.Boolean(), nullable=False, default=True, server_default="true")
    rqsub = sa.Column("rqsub", sa.String(20), nullable=False)
    rqprc = sa.Column("rqprc", sa.Numeric(38, 2), nullable=False, default=0, server_default="0")
    is_active = sa.Column(sa.Boolean(), nullable=False, default=True, server_default="true")
    isfxd = sa.Column("isfxd", sa.Boolean())
    rqatt = sa.Column("rqatt", sa.String())
