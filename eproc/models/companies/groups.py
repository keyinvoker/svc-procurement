import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class Group(BaseModel):
    __tablename__ = "groups"

    id = sa.Column(sa.String(20), primary_key=True)
    entity_id = sa.Column(sa.String(10), sa.ForeignKey("entities.id"), nullable=False)
    description = sa.Column(sa.String(100), nullable=False)
    is_active = sa.Column(sa.Boolean(), nullable=False)

    entity = db.relationship(
        "Entity", backref=backref(__tablename__, uselist=False)
    )
