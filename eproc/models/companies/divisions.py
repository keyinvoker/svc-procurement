import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class Division(BaseModel):
    __tablename__ = "divisions"

    id = sa.Column(sa.String(), primary_key=True)
    entity_id = sa.Column(sa.String(10), sa.ForeignKey("entities.id"), nullable=False)
    description = sa.Column(sa.String(500), nullable=False)
    is_active = sa.Column(sa.Boolean(), nullable=False)

    entity = db.relationship(
        "Entity", backref=backref(__tablename__, uselist=False)
    )
