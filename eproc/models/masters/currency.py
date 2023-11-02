import sqlalchemy as sa

from eproc.models.base_model import BaseModel


class Currency(BaseModel):
    __tablename__ = "currencies"

    id = sa.Column(sa.String(10), primary_key=True)
    description = sa.Column(sa.String(100))
    symbol = sa.Column(sa.String(10))
    isbsc = sa.Column(sa.Boolean(), nullable=False, default=False, server_default="false")
    is_active = sa.Column(sa.Boolean(), nullable=False, default=True, server_default="true")
