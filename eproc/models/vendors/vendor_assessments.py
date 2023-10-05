import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class VendorAssessment(BaseModel):
    __tablename__ = "vendor_assessments"

    id = sa.Column(sa.BigInteger(), primary_key=True)
    vendor_id = sa.Column(sa.String(24), sa.ForeignKey("vendors.id"), nullable=False)
    assessor_user_id = sa.Column(sa.String(20), sa.ForeignKey("users.id"), nullable=False)
    reference_id = sa.Column(sa.Integer(), sa.ForeignKey("references.id"), nullable=False)
    assessment_notes = sa.Column(sa.String(5000), nullable=False)

    vendor = db.relationship(
        "Vendor", backref=backref(__tablename__, uselist=False)
    )
    assessor = db.relationship(
        "User", backref=backref(__tablename__, uselist=False)
    )
    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
