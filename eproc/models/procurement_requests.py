import sqlalchemy as sa
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import BaseModel


class ProcurementRequest(BaseModel):
    __tablename__ = "procurement_requests"

    # TODO benerin table
    id = sa.Column("trnno", sa.String(), primary_key=True)
    branch_id = sa.Column("brcid", sa.String(), sa.ForeignKey("branches.id"), nullable=False)
    directorate_id = sa.Column("dirid", sa.String(20), sa.ForeignKey("directorates.id"), nullable=False)
    division_id = sa.Column("divid", sa.String(), sa.ForeignKey("divisions.id"), nullable=False)
    department_id = sa.Column("depid", sa.String(), sa.ForeignKey("departments.id"), nullable=False)
    dapid = sa.Column("dapid", sa.String(), nullable=False)  # TODO: Foreign Key
    flag1 = sa.Column(sa.String(15))
    flag2 = sa.Column(sa.String(15))
    transaction_date = sa.Column("trndt", sa.DateTime(), nullable=False)
    transaction_type = sa.Column("trnty", sa.String(4), nullable=False)
    period = sa.Column("fisyr", sa.Integer(), nullable=False)
    fismn = sa.Column("fismn", sa.Integer(), nullable=False)
    catcd = sa.Column("catcd", sa.String(10))
    grpcd = sa.Column("grpcd", sa.String(10))
    sqenc = sa.Column("sqenc", sa.Integer(), nullable=False)
    document_number = sa.Column("docno", sa.String(20))
    coacd = sa.Column("coacd", sa.String(20))
    allcn = sa.Column("allcn", sa.String(50))

    isugn = sa.Column("isugn", sa.Integer(), nullable=False)  # TODO: change to boolean
    is_ugn = column_property(
        case((isugn == 1, True), else_=False)
    )

    ndsfr = sa.Column("ndsfr", sa.String(20))
    ndsto = sa.Column("ndsto", sa.String(20))
    description = sa.Column("descr", sa.String(500))
    requester_user_id = sa.Column("reqby", sa.String(), sa.ForeignKey("users.id"), nullable=False)
    entby = sa.Column("entby", sa.String(), nullable=False)  # TODO: Foreign Key
    redto = sa.Column("redto", sa.String(30))
    alcto = sa.Column("alcto", sa.String(30))
    reference_id = sa.Column("stats", sa.Integer(), sa.ForeignKey("references.id"))
    appsc = sa.Column("appsc", sa.String(20))
    dref1 = sa.Column("dref1", sa.String(100))
    dref2 = sa.Column("dref2", sa.String(100))
    dref3 = sa.Column("dref3", sa.String(100))
    dref4 = sa.Column("dref4", sa.String(100))
    dref5 = sa.Column("dref5", sa.String(100))
    dref6 = sa.Column("dref6", sa.String(100))
    temps = sa.Column("temps", sa.String(100))

    requester = db.relationship(
        "User", backref=backref(__tablename__, uselist=False)
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
