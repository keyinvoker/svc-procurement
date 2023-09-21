import sqlalchemy as sa

from eproc.models.base_model import BaseModel


class Department(BaseModel):
    __tablename__ = "departments"

    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text(), default=None)
    is_approved = sa.Column(
        sa.Boolean(),
        default=False,
        server_default="false",
    )
