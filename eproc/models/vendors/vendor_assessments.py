import sqlalchemy as sa
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import BaseModel


class VendorAssessment(BaseModel):
    __tablename__ = "vendor_assessments"

    id = sa.Column("apvno", sa.Integer(), primary_key=True)
    vendor_id = sa.Column(sa.String(), sa.ForeignKey("vendors.id"), nullable=False)
    assessor_user_id = sa.Column(sa.String(), sa.ForeignKey("users.id"), nullable=False)
    reference_id = sa.Column("stats", sa.Integer(), sa.ForeignKey("references.id"))
    assessment_notes = sa.Column("apvnt", sa.String(5000))
    # reviewed_at = sa.Column(sa.DateTime(), nullable=False)  # TODO: pake created_at aja

    vendor = db.relationship(
        "Vendor", backref=backref(__tablename__, uselist=False)
    )
    assessor = db.relationship(
        "User", backref=backref(__tablename__, uselist=False)
    )
    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
