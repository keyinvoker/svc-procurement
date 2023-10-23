import sqlalchemy as sa

from eproc.models.base_model import BaseModel


class ItemClass(BaseModel):
    __tablename__ = "item_classes"

    id = sa.Column(sa.String(10), primary_key=True)
    description = sa.Column(sa.String(100), nullable=False)
    is_active = sa.Column(sa.Boolean(), nullable=False, default=True, server_default="true")
