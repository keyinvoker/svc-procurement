import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class Department(BaseModel):
    __tablename__ = "departments"

    id = sa.Column(sa.String(20), primary_key=True)
    entity_id = sa.Column(sa.String(10), sa.ForeignKey("entities.id"), nullable=False)
    description = sa.Column(sa.String(500), nullable=False)
    updated_by = sa.Column(sa.String(), default="auto from HC", server_default="auto from HC")
    is_active = sa.Column(sa.Boolean(), nullable=False)

    entity = db.relationship(
        "Entity", backref=backref(__tablename__, uselist=False)
    )
