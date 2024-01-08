import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class PettyCashClaimAssessment(BaseModel):
    __tablename__ = "petty_cash_claim_assessments"

    id = sa.Column(sa.BigInteger(), primary_key=True)
    petty_cash_claim_id = sa.Column(sa.String(24), sa.ForeignKey("petty_cash_claims.id"), nullable=False)
    assessor_user_id = sa.Column(sa.String(20), sa.ForeignKey("users.id"), nullable=False)
    reference_id = sa.Column(sa.Integer(), sa.ForeignKey("references.id"), nullable=False, default=0, server_default="0")
    assessment_notes = sa.Column(sa.String(5000), nullable=False)

    petty_cash_claim = db.relationship(
        "PettyCashClaim", backref=backref(__tablename__, uselist=False)
    )
    assessor = db.relationship(
        "User", backref=backref(__tablename__, uselist=False)
    )
    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
