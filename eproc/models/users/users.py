import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import (
    BaseModel,
    WIBNow,
    wibnow,
)


class User(BaseModel):
    __tablename__ = "users"

    id = sa.Column(sa.String(24), primary_key=True)
    reference_id = sa.Column(sa.Integer(), sa.ForeignKey("references.id"), nullable=False)
    first_approver_id = sa.Column(sa.String(10))
    second_approver_id = sa.Column(sa.String(10))
    third_approver_id = sa.Column(sa.String(10))
    app_id = sa.Column(sa.String(10), nullable=False)
    username = sa.Column(sa.String(24), nullable=False)  # TODO: REDUNDANT :: same value as `usrid`; delete?
    full_name = sa.Column(sa.String(50))
    password = sa.Column(sa.String(32), nullable=False)
    password_length = sa.Column(sa.Integer(), nullable=False)
    password_salt = sa.Column(sa.String(120))  # TODO: REDUNDANT: unused
    password_hash = sa.Column(sa.String(120))  # TODO: DANGEROUS: bukan hash ini?!?!?!; clear text password!!!
    password_question = sa.Column(sa.String(120))  # TODO: REDUNDANT: unused
    password_answer = sa.Column(sa.String(120))  # TODO: REDUNDANT: unused
    security_status = sa.Column(sa.String(10))  # TODO: REDUNDANT: unused
    email = sa.Column(sa.String(200))

    is_email_confirmed = sa.Column(sa.Boolean(), nullable=False)
    is_anonymous = sa.Column(sa.Boolean(), nullable=False)
    is_admin = sa.Column(sa.Boolean(), nullable=False)
    is_head_office_user = sa.Column(sa.Boolean(), nullable=False)
    is_kpw_user = sa.Column(sa.Boolean(), nullable=False)
    is_branch_user = sa.Column(sa.Boolean(), nullable=False)
    is_approved = sa.Column(sa.Boolean(), nullable=False, default=False, server_default="false")
    is_locked = sa.Column(sa.Boolean(), nullable=False)
    is_phone_number_confirmed = sa.Column(sa.Boolean(), nullable=False)
    remember_me = sa.Column(sa.Boolean(), nullable=False)
    two_factor_enabled = sa.Column(sa.Boolean(), nullable=False)
    lock_enabled = sa.Column(sa.Boolean(), nullable=False)

    captcha = sa.Column(sa.String(6))  # TODO: REDUNDANT
    mobile_pin = sa.Column(sa.String(16))
    mobile_alias = sa.Column(sa.String(16))

    last_active_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    last_login_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    last_lock_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    last_password_change_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )

    comment = sa.Column(sa.String(256))
    phone_number = sa.Column(sa.String(100))
    valid_until = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    acfct = sa.Column("acfct", sa.Integer(), nullable=False)
    flag1 = sa.Column(sa.String(15))
    flag2 = sa.Column(sa.String(15))
    temps = sa.Column(sa.String(100))

    is_active = sa.Column(sa.Boolean(), nullable=False, default=False, server_default="false")

    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
