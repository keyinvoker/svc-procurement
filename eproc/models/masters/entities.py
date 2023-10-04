import sqlalchemy as sa

from eproc.models.base_model import BaseModel


class Entity(BaseModel):
    __tablename__ = "entities"

    id = sa.Column(sa.String(), primary_key=True)
    description = sa.Column(sa.String(100), nullable=False)
    is_active = sa.Column(sa.Boolean())
