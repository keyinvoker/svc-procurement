import sqlalchemy as sa
from sqlalchemy.orm import column_property
from sqlalchemy.sql import case

from eproc.models.base_model import BaseModel


class VendorReview(BaseModel):
    __tablename__ = "vendor_reviews"

    id = sa.Column("apvno", sa.Integer(), primary_key=True)
    vendor_id = sa.Column("vdrid", sa.String(), nullable=False)  # TODO Foreign Key
    status_id = sa.Column("stats", sa.Integer())  # TODO Foreign Key
    review_notes = sa.Column("apvnt", sa.String(5000))
    reviewer_user_id = sa.Column("apvun", sa.String(), nullable=False)
    # reviewed_at = sa.Column(sa.DateTime(), nullable=False)  # TODO: pake created_at aja
