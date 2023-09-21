import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class AuditTrail(BaseModel):
    __tablename__ = "audit_trails"

    admin_id = sa.Column(
        sa.BigInteger,
        sa.ForeignKey("admins.id"),
        nullable=True
    )
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text(), default=None)
    is_approved = sa.Column(
        sa.Boolean(),
        default=False,
        server_default="false",
    )

    admin = db.relationship(
        "User", backref=backref(__tablename__, uselist=False)
    )
