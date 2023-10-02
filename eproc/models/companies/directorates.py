import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import BIT
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import BaseModel


class Directorate(BaseModel):
    __tablename__ = "directorates"

    id = sa.Column(sa.String(), primary_key=True)
    description = sa.Column("descr", sa.String(500), nullable=False)
    entity_id = sa.Column("nttid", sa.String(10), sa.ForeignKey("entities.id"), nullable=False)

    is_active = sa.Column("isact", sa.Boolean())  # TODO: change to boolean (from BIT)

    entity = db.relationship(
        "Entity", backref=backref(__tablename__, uselist=False)
    )
