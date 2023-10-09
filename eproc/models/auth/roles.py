import sqlalchemy as sa

from eproc.models.base_model import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"

    id = sa.Column(sa.String(10), primary_key=True)
    description = sa.Column(sa.String(500), nullable=False)
    is_active = sa.Column(sa.Boolean(), nullable=False)
