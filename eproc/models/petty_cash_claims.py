import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel, WIBNow
from eproc.helpers.commons import wibnow


class PettyCashClaim(BaseModel):
    __tablename__ = "petty_cash_claims"

    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True)
    item_class_id = sa.Column(sa.String(10), sa.ForeignKey("item_classes.id"), nullable=False)
    item_category_id = sa.Column(sa.String(10), sa.ForeignKey("item_categories.id"), nullable=False)
    branch_id = sa.Column(sa.String(20), sa.ForeignKey("branches.id"), nullable=False)
    preparer_id = sa.Column(sa.String(30), sa.ForeignKey("users.id"), nullable=False)
    requester_id = sa.Column(sa.String(), sa.ForeignKey("employees.id"), nullable=False)
    cost_center_id = sa.Column(sa.String(20), sa.ForeignKey("cost_centers.id"))
    reference_id = sa.Column(sa.Integer(), sa.ForeignKey("references.id"), nullable=False, default=0, server_default="0")
    transaction_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    year = sa.Column(sa.Integer(), nullable=False)
    month = sa.Column(sa.Integer(), nullable=False)
    sequence_number = sa.Column(sa.Integer(), nullable=False)
    document_number = sa.Column(sa.String(20))
    description = sa.Column(sa.String(500))
    required_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    app_source = sa.Column(sa.String(20), default="epro", server_default="epro")
    dref1 = sa.Column(sa.String(200))
    dref2 = sa.Column(sa.String(200))
    dref3 = sa.Column(sa.String(200))
    dref4 = sa.Column(sa.String(200))
    dref5 = sa.Column(sa.String(200))
    dref6 = sa.Column(sa.String(200))
    flag1 = sa.Column(sa.String(15))
    flag2 = sa.Column(sa.String(15))
    temps = sa.Column(sa.String(100))

    item_class = db.relationship(
        "ItemClass", backref=backref(__tablename__, uselist=False)
    )
    item_category = db.relationship(
        "ItemCategory", backref=backref(__tablename__, uselist=False)
    )
    branch = db.relationship(
        "Branch", backref=backref(__tablename__, uselist=False)
    )
    cost_center = db.relationship(
        "CostCenter", backref=backref(__tablename__, uselist=False)
    )
    preparer = db.relationship(
        "User", backref=backref(__tablename__, uselist=False)
    )
    requester = db.relationship(
        "Employee", backref=backref(__tablename__, uselist=False)
    )
    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
