import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class Link(BaseModel):
    __tablename__ = "links"

    id = sa.Column(sa.BigInteger(), primary_key=True)
    user_id = sa.Column(sa.String(12), sa.ForeignKey("users.id"), nullable=False)
    refid = sa.Column("refid", sa.String(100), nullable=False)  # TODO: Foreign Key to what table?
    url = sa.Column(sa.String(250), nullable=False)
    description = sa.Column(sa.String(1000), nullable=False)
    module = sa.Column(sa.String(100), nullable=False)
    password = sa.Column(sa.String(32), nullable=False)
    mail_to = sa.Column(sa.String(1000))
    mail_cc = sa.Column(sa.String(2500))
    mail_subject = sa.Column(sa.String(1000))
    mail_content = sa.Column(sa.String(500000))
    mail_attachment = sa.Column(sa.String(500000))

    user = db.relationship(
        "User", backref=backref(__tablename__, uselist=False)
    )
