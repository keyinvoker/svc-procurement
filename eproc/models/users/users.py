import sqlalchemy as sa
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import (
    BaseModel,
    WIBNow,
    wibnow,
)


class User(BaseModel):
    __tablename__ = "users"

    id = sa.Column(sa.String(24), primary_key=True)
    reference_id = sa.Column(sa.Integer(), sa.ForeignKey("references.id"))
    first_approver_id = sa.Column(sa.String())
    second_approver_id = sa.Column(sa.String())
    third_approver_id = sa.Column(sa.String())
    app_id = sa.Column(sa.String(10), nullable=False)
    username = sa.Column(sa.String(24), nullable=False)  # TODO: REDUNDANT :: same value as `usrid`; delete?
    full_name = sa.Column(sa.String(50))
    password = sa.Column(sa.String(32), nullable=False)
    password_length = sa.Column(sa.Integer(), nullable=False)
    password_salt = sa.Column(sa.String(120))
    password_hash = sa.Column(sa.String(120))
    password_question = sa.Column(sa.String(120))
    password_answer = sa.Column(sa.String(120))
    security_status = sa.Column(sa.String(10))
    email = sa.Column(sa.String(200))

    is_email_confirmed = sa.Column(sa.Boolean(), nullable=False)
    is_anonymous = sa.Column(sa.Boolean(), nullable=False)
    is_admin = sa.Column(sa.Boolean(), nullable=False)
    is_head_office_user = sa.Column(sa.Boolean(), nullable=False)
    is_kpw_user = sa.Column(sa.Boolean(), nullable=False)
    is_branch_user = sa.Column(sa.Boolean(), nullable=False)
    is_approved = sa.Column(sa.Boolean(), nullable=False)
    is_locked = sa.Column(sa.Boolean(), nullable=False)
    is_phone_number_confirmed = sa.Column(sa.Boolean(), nullable=False)
    remember_me = sa.Column(sa.Boolean(), nullable=False)
    two_factor_enabled = sa.Column(sa.Boolean(), nullable=False)
    lock_enabled = sa.Column(sa.Boolean(), nullable=False)
    # emcon = sa.Column("emcon", sa.Integer(), default=0)  # TODO: change to boolean
    # is_email_confirmed = column_property(case(
    #     (emcon == 1, True), else_=False
    # ))
    # isann = sa.Column("isann", sa.Integer(), default=0)  # TODO: change to boolean
    # is_anonymous = column_property(case(
    #     (isann == 1, True), else_=False
    # ))
    # isadm = sa.Column("isadm", sa.Integer(), default=0)  # TODO: change to boolean
    # is_admin = column_property(case(
    #     (isadm == 1, True), else_=False
    # ))
    # isuho = sa.Column("isuho", sa.Integer(), default=1)  # TODO: change to boolean
    # is_head_office_user = column_property(case(
    #     (isuho == 1, True), else_=False
    # ))
    # isukp = sa.Column("isukp", sa.Integer(), default=0)  # TODO: change to boolean
    # is_kpw_user = column_property(case(
    #     (isukp == 1, True), else_=False
    # ))
    # isust = sa.Column("isust", sa.Integer(), default=0)  # TODO: change to boolean
    # is_branch_user = column_property(case(
    #     (isukp == 1, True), else_=False
    # ))
    # isapr = sa.Column("isapr", sa.Integer(), default=0)  # TODO: change to boolean
    # is_approved = column_property(case(
    #     (isapr == 1, True), else_=False
    # ))
    # islck = sa.Column("islck", sa.Integer(), default=0)  # TODO: change to boolean
    # is_locked = column_property(case(
    #     (islck == 1, True), else_=False
    # ))
    # remme = sa.Column("remme", sa.Integer(), default=0)  # TODO: change to boolean
    # remember_me = column_property(
    #     case((remme == 1, True), else_=False)
    # )
    # phonc = sa.Column("phonc", sa.Integer(), default=0)  # TODO: change to boolean
    # is_phone_number_confirmed = column_property(
    #     case((phonc == 1, True), else_=False)
    # )
    # tface = sa.Column("tface", sa.Integer(), default=0)  # TODO: change to boolean
    # two_factor_enabled = column_property(
    #     case((tface == 1, True), else_=False)
    # )
    # locen = sa.Column("locen", sa.Integer(), default=0)  # TODO: change to boolean
    # lock_enabled = column_property(
    #     case((locen == 1, True), else_=False)
    # )

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
    acfct = sa.Column(sa.Integer())
    flag1 = sa.Column(sa.String(15))
    flag2 = sa.Column(sa.String(15))
    temps = sa.Column(sa.String(100))

    is_active = sa.Column(sa.Boolean(), nullable=False)

    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
