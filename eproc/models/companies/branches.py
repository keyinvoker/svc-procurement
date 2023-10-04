import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class Branch(BaseModel):
    __tablename__ = "branches"

    id = sa.Column(sa.String(), primary_key=True)
    entity_id = sa.Column(sa.String(10), sa.ForeignKey("entities.id"), nullable=False)
    description = sa.Column(sa.String(500), nullable=False)
    first_address = sa.Column(sa.String(150))
    second_address = sa.Column(sa.String(150))
    third_address = sa.Column(sa.String(150))
    city = sa.Column(sa.String(100))
    province = sa.Column(sa.String(100))
    country = sa.Column(sa.String(100))
    phone_number = sa.Column(sa.String(20))
    fax_number = sa.Column(sa.String(20))
    capsp = sa.Column(sa.String(10))
    capct = sa.Column(sa.String(10))
    carct = sa.Column(sa.String(10))
    crtct = sa.Column(sa.String(10))
    is_active = sa.Column(sa.Boolean())

    entity = db.relationship(
        "Entity", backref=backref(__tablename__, uselist=False)
    )
