import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel, WIBNow
from eproc.helpers.commons import wibnow


class Employee(BaseModel):
    __tablename__ = "employees"

    id = sa.Column(sa.String(), primary_key=True)
    entity_id = sa.Column(sa.String(10), sa.ForeignKey("entities.id"), nullable=False)
    regional_id = sa.Column(sa.String(10), sa.ForeignKey("regionals.id"), nullable=False)
    branch_id = sa.Column(sa.String(20), sa.ForeignKey("branches.id"), nullable=False)
    directorate_id = sa.Column(sa.String(20), sa.ForeignKey("directorates.id"), nullable=False)
    division_id = sa.Column(sa.String(20), sa.ForeignKey("divisions.id"), nullable=False)
    department_id = sa.Column(sa.String(20), sa.ForeignKey("departments.id"), nullable=False)
    group_id = sa.Column(sa.String(20), sa.ForeignKey("groups.id"), nullable=False)
    postn = sa.Column("postn", sa.String(20), nullable=False)  # TODO: Foreign Key (?)
    cost_center_id = sa.Column(sa.String(20), sa.ForeignKey("cost_centers.id"))
    first_approver_id = sa.Column(sa.String(10))
    second_approver_id = sa.Column(sa.String(10))
    third_approver_id = sa.Column(sa.String(10))
    untid = sa.Column("untid", sa.String(20), nullable=False)
    full_name = sa.Column(sa.String(50))
    email = sa.Column(sa.String(200))
    phone_number = sa.Column(sa.String(20))
    identity_number = sa.Column(sa.String(20))
    gender = sa.Column(sa.String(20))
    join_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    leave_date = sa.Column(sa.DateTime(timezone=True))
    is_active = sa.Column(sa.Boolean(), nullable=False)

    entity = db.relationship(
        "Entity", backref=backref(__tablename__, uselist=False)
    )
    regional = db.relationship(
        "Regional", backref=backref(__tablename__, uselist=False)
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
    group = db.relationship(
        "Group", backref=backref(__tablename__, uselist=False)
    )
    cost_center = db.relationship(
        "CostCenter", backref=backref(__tablename__, uselist=False)
    )
