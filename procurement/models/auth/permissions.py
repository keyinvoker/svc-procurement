import sqlalchemy as sa

from procurement.models.base_model import BaseModel


class Permission(BaseModel):
    __tablename__ = "permissions"

    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text(), default=None)
