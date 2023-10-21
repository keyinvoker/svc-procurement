import sqlalchemy as sa

from eproc.models.base_model import BaseModel


class Reference(BaseModel):
    __tablename__ = "references"

    id = sa.Column(sa.Integer(), primary_key=True)
    refid = sa.Column("refid", sa.String(20), nullable=False)
    parameter_value = sa.Column(sa.Numeric(18, 2), nullable=False)
    parameter_text = sa.Column(sa.String(100))
    description = sa.Column(sa.String(1000), nullable=False)
    order_number = sa.Column(sa.BigInteger(), nullable=False)
    rsign = sa.Column("rsign", sa.String(12))
    dref1 = sa.Column(sa.String(20))
    dref2 = sa.Column(sa.String(200))
    dref3 = sa.Column(sa.String(20))
    is_active = sa.Column(sa.Boolean(), default=True, server_default="true")
