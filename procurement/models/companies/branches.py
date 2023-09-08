import sqlalchemy as sa
from sqlalchemy.orm import backref

from procurement import db
from procurement.models.base_model import BaseModel


class Branch(BaseModel):
    __tablename__ = "branches"

    role_id = sa.Column(
        sa.BigInteger,
        sa.ForeignKey("roles.id"),
        nullable=True
    )
    code = sa.Column(sa.String(255), nullable=False)
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text(), default=None)
    is_approved = sa.Column(
        sa.Boolean(),
        default=False,
        server_default="false",
    )

    role = db.relationship(
        "Role", backref=backref(__tablename__, uselist=False)
    )
