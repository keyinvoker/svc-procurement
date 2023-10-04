import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import BIT
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import BaseModel


class Department(BaseModel):
    __tablename__ = "departments"

    id = sa.Column(sa.String(), primary_key=True)
    entity_id = sa.Column(sa.String(10), sa.ForeignKey("entities.id"), nullable=False)
    description = sa.Column(sa.String(500), nullable=False)
    updated_by = sa.Column(sa.String(), default="auto from HC", server_default="auto from HC")
    is_active = sa.Column(sa.Boolean())

    entity = db.relationship(
        "Entity", backref=backref(__tablename__, uselist=False)
    )
