import sqlalchemy as sa

from eproc.models.base_model import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"

    code = sa.Column(sa.String(255), nullable=False)
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text(), default=None)
    is_approved = sa.Column(sa.Boolean())
