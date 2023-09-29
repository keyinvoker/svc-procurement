import sqlalchemy as sa
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import BaseModel


class Employee(BaseModel):
    __tablename__ = "employees"

    id = sa.Column(sa.String(), primary_key=True)
    full_name = sa.Column("empnm", sa.String())
    postn = sa.Column("postn", sa.String(20), nullable=False)
    nttid = sa.Column("nttid", sa.String(10), nullable=False)
    rgnid = sa.Column("rgnid", sa.String(10))
    branch_id = sa.Column("brcid", sa.String(20), sa.ForeignKey("branches.id"), nullable=False)
    directorate_id = sa.Column("dirid", sa.String(20), nullable=False)  # TODO: Foreign Key
    division_id = sa.Column("divid", sa.String(20), sa.ForeignKey("divisions.id"), nullable=False)
    department_id = sa.Column("depid", sa.String(20), sa.ForeignKey("departments.id"), nullable=False)
    coacd = sa.Column("coacd", sa.String(20))
    email = sa.Column("email", sa.String(200))
    phone_number = sa.Column("phono", sa.String(20))
    identity_number = sa.Column("noktp", sa.String(20))
    gender = sa.Column("gendr", sa.String(20))
    join_date = sa.Column("joidt", sa.DateTime())
    leave_date = sa.Column("outdt", sa.DateTime())
    first_approver_id = sa.Column("ldid1", sa.String(10))
    second_approver_id = sa.Column("ldid2", sa.String(10))
    third_approver_id = sa.Column("ldid3", sa.String(10))
    group_id = sa.Column("grpid", sa.String(20), nullable=False)
    untid = sa.Column("untid", sa.String(20), nullable=False)

    isact = sa.Column("isact", sa.Integer(), default=0)  # TODO: change to boolean
    is_active = column_property(
        case((isact == 1, True), else_=False)
    )

    branch = db.relationship(
        "Branch", backref=backref(__tablename__, uselist=False)
    )
    division = db.relationship(
        "Division", backref=backref(__tablename__, uselist=False)
    )
    department = db.relationship(
        "Department", backref=backref(__tablename__, uselist=False)
    )
