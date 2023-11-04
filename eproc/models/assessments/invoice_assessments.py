import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class InvoiceAssessment(BaseModel):
    __tablename__ = "invoice_assessments"

    id = sa.Column(sa.BigInteger(), primary_key=True)
    invoice_id = sa.Column(sa.String(24), sa.ForeignKey("invoices.id"), nullable=False)
    assessor_user_id = sa.Column(sa.String(20), sa.ForeignKey("users.id"), nullable=False)
    reference_id = sa.Column(sa.Integer(), sa.ForeignKey("references.id"), nullable=False, default=0, server_default="0")
    assessment_notes = sa.Column(sa.String(5000), nullable=False)

    invoice = db.relationship(
        "Invoice", backref=backref(__tablename__, uselist=False)
    )
    assessor = db.relationship(
        "User", backref=backref(__tablename__, uselist=False)
    )
    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
