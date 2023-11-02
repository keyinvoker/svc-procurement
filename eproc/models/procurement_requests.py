import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel, WIBNow
from eproc.helpers.commons import wibnow


class ProcurementRequest(BaseModel):
    __tablename__ = "procurement_requests"

    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True)
    item_class_id = sa.Column(sa.String(10), sa.ForeignKey("item_classes.id"), nullable=False)
    item_category_id = sa.Column(sa.String(10), sa.ForeignKey("item_categories.id"), nullable=False)
    branch_id = sa.Column(sa.String(), sa.ForeignKey("branches.id"), nullable=False)
    directorate_id = sa.Column(sa.String(20), sa.ForeignKey("directorates.id"), nullable=False)
    division_id = sa.Column(sa.String(), sa.ForeignKey("divisions.id"), nullable=False)
    department_id = sa.Column(sa.String(), sa.ForeignKey("departments.id"), nullable=False)
    cost_center_id = sa.Column(sa.String(20), sa.ForeignKey("cost_centers.id"))
    reference_id = sa.Column(sa.Integer(), sa.ForeignKey("references.id"), nullable=False, default=0, server_default="0")
    preparer_id = sa.Column(sa.String(30), sa.ForeignKey("users.id"), nullable=False)
    requester_id = sa.Column(sa.String(), sa.ForeignKey("employees.id"), nullable=False)
    transaction_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    transaction_type = sa.Column(sa.String(4), nullable=False)
    year = sa.Column(sa.Integer(), nullable=False)
    month = sa.Column(sa.Integer(), nullable=False)
    description = sa.Column(sa.String(500))
    document_number = sa.Column(sa.String(20))
    app_source = sa.Column(sa.String(20))
    is_ugn = sa.Column(sa.Boolean(), nullable=False, default=False, server_default="false")

    allcn = sa.Column("allcn", sa.String(50))
    ndsfr = sa.Column("ndsfr", sa.String(20))
    ndsto = sa.Column("ndsto", sa.String(20))
    redto = sa.Column("redto", sa.String(30))
    alcto = sa.Column("alcto", sa.String(30))

    sequence_number = sa.Column(sa.Integer(), nullable=False)
    dref1 = sa.Column(sa.String(100))
    dref2 = sa.Column(sa.String(100))
    dref3 = sa.Column(sa.String(100))
    dref4 = sa.Column(sa.String(100))
    dref5 = sa.Column(sa.String(100))
    dref6 = sa.Column(sa.String(100))
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
    directorate = db.relationship(
        "Directorate", backref=backref(__tablename__, uselist=False)
    )
    division = db.relationship(
        "Division", backref=backref(__tablename__, uselist=False)
    )
    department = db.relationship(
        "Department", backref=backref(__tablename__, uselist=False)
    )
    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
    preparer = db.relationship(
        "User", backref=backref(__tablename__, uselist=False)
    )
    requester = db.relationship(
        "Employee", backref=backref(__tablename__, uselist=False)
    )
    cost_center = db.relationship(
        "CostCenter", backref=backref(__tablename__, uselist=False)
    )
