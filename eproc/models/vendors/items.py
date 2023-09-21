import sqlalchemy as sa

from eproc.models.base_model import BaseModel


class Item(BaseModel):
    __tablename__ = "items"

    category = sa.Column(sa.String(255), nullable=False)
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text(), default=None)
