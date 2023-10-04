import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import BIT
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case
from sqlalchemy.ext.hybrid import hybrid_property


from eproc.models.base_model import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"

    id = sa.Column(sa.String(), primary_key=True)
    description = sa.Column(sa.String(500), nullable=False)
    is_active = sa.Column(sa.Boolean(), nullable=False)
