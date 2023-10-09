import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class UserRole(BaseModel):
    __tablename__ = "users_roles"

    _no_primary_key = sa.Column(sa.Integer(), primary_key=True)
    user_id = sa.Column(sa.String(), sa.ForeignKey("users.id"), nullable=False)
    role_id = sa.Column(sa.String(), sa.ForeignKey("roles.id"), nullable=False)

    user = db.relationship(
        "User", backref=backref(__tablename__, uselist=False)
    )
    role = db.relationship(
        "Role", backref=backref(__tablename__, uselist=False)
    )
