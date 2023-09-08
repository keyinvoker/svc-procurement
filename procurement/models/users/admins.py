import sqlalchemy as sa
from sqlalchemy.orm import backref

from procurement import db
from procurement.models.base_model import BaseModel


class Admin(BaseModel):
    __tablename__ = "admins"

    role_id = sa.Column(
        sa.BigInteger,
        sa.ForeignKey("roles.id"),
        nullable=True
    )
    name = sa.Column(sa.String(255), nullable=False)
    employee_identification_number = sa.Column(sa.String(255), nullable=False)
    email = sa.Column(sa.String(255), nullable=False, unique=True)
    password = sa.Column(sa.String(255), nullable=False)
    salt = sa.Column(sa.String(225), nullable=False)
    password_updated_at = sa.Column(sa.DateTime(), default=None)
    is_approved = sa.Column(
        sa.Boolean(),
        default=False,
        server_default="false",
    )

    role = db.relationship(
        "Role", backref=backref(__tablename__, uselist=False)
    )
    # TODO: correct relationship?
    # division = db.relationship(
    #     "Division", backref=backref(__tablename__, uselist=False)
    # )
