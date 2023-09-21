import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class RolePermission(BaseModel):
    __tablename__ = "roles_permissions"

    role_id = sa.Column(
        sa.BigInteger,
        sa.ForeignKey("roles.id")
    )
    permission_id = sa.Column(
        sa.BigInteger,
        sa.ForeignKey("permissions.id")
    )

    role = db.relationship(
        "Role", backref=backref(__tablename__, uselist=False)
    )
    permission = db.relationship(
        "Permission", backref=backref(__tablename__, uselist=False)
    )
