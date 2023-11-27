import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class RoleMenu(BaseModel):
    __tablename__ = "roles_menus"

    role_id = sa.Column(sa.String(10), sa.ForeignKey("roles.id"), nullable=False, primary_key=True)
    menu_id = sa.Column(sa.String(12), sa.ForeignKey("menus.id"), nullable=False, primary_key=True)
    aladd = sa.Column(sa.Boolean(), nullable=False)
    aledt = sa.Column(sa.Boolean(), nullable=False)
    aldel = sa.Column(sa.Boolean(), nullable=False)
    alexc = sa.Column(sa.Boolean(), nullable=False)
    alsnc = sa.Column(sa.Boolean(), nullable=False)
    alpos = sa.Column(sa.Boolean(), nullable=False)
    alups = sa.Column(sa.Boolean(), nullable=False)
    alaap = sa.Column(sa.Boolean(), nullable=False)
    alapp = sa.Column(sa.Boolean(), nullable=False)
    alrej = sa.Column(sa.Boolean(), nullable=False)
    altsk = sa.Column(sa.Boolean(), nullable=False, default=False, server_default="false")
    alprn = sa.Column(sa.Boolean(), nullable=False, default=False, server_default="false")

    role = db.relationship(
        "Role", backref=backref(__tablename__, uselist=False)
    )
    menu = db.relationship(
        "Menu", backref=backref(__tablename__, uselist=False)
    )
