import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import BIT
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc.models.base_model import BaseModel


class Entity(BaseModel):
    __tablename__ = "entities"

    id = sa.Column(sa.String(), primary_key=True)
    description = sa.Column("descr", sa.String(100), nullable=False)

    is_active = sa.Column("isact", sa.Boolean())  # TODO: change to boolean (from BIT)
