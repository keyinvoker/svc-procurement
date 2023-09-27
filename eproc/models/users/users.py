import sqlalchemy as sa
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = sa.Column(sa.String(), primary_key=True)
    app_id = sa.Column("appid", sa.String())
    username = sa.Column("uname", sa.String())  # TODO: delete later, because literally same as `usrid`
    full_name = sa.Column("ffnam", sa.String())
    password = sa.Column("paswd", sa.String())
    password_length = sa.Column("pasfm", sa.Integer())
    password_salt = sa.Column("passt", sa.String())
    password_hash = sa.Column("pashs", sa.String())
    password_question = sa.Column("pasqs", sa.String())
    password_answer = sa.Column("pasaw", sa.String())
    security_status = sa.Column("secst", sa.String(10))
    email = sa.Column("email", sa.String())
    emcon = sa.Column("emcon", sa.Integer(), default=0)  # TODO: change to boolean
    is_email_confirmed = column_property(case(
        (emcon == 1, True), else_=False
    ))
    isann = sa.Column("isann", sa.Integer(), default=0)  # TODO: change to boolean
    is_anonymous = column_property(case(
        (isann == 1, True), else_=False
    ))
    isadm = sa.Column("isadm", sa.Integer(), default=0)  # TODO: change to boolean
    is_admin = column_property(case(
        (isadm == 1, True), else_=False
    ))
    isuho = sa.Column("isuho", sa.Integer(), default=1)  # TODO: change to boolean
    is_head_office_user = column_property(case(
        (isuho == 1, True), else_=False
    ))
    isukp = sa.Column("isukp", sa.Integer(), default=0)  # TODO: change to boolean
    is_kpw_user = column_property(case(
        (isukp == 1, True), else_=False
    ))
    isust = sa.Column("isust", sa.Integer(), default=0)  # TODO: change to boolean
    is_branch_user = column_property(case(
        (isukp == 1, True), else_=False
    ))
    isapr = sa.Column("isapr", sa.Integer(), default=0)  # TODO: change to boolean
    is_approved = column_property(case(
        (isapr == 1, True), else_=False
    ))
    islck = sa.Column("islck", sa.Integer(), default=0)  # TODO: change to boolean
    is_locked = column_property(case(
        (islck == 1, True), else_=False
    ))
    captcha = sa.Column("sapsa", sa.String(6))  # TODO: idk wtf for ???
    mobile_pin = sa.Column("mopin", sa.String(16))
    mobile_alias = sa.Column("moals", sa.String(16))
    last_active_date = sa.Column("ladat", sa.DateTime())
    last_login_date = sa.Column("llgdt", sa.DateTime())
    last_lock_date = sa.Column("llkdt", sa.DateTime())
    last_password_change_date = sa.Column("lpcdt", sa.DateTime())
    comment = sa.Column("comnt", sa.String())
    phone_number = sa.Column("phono", sa.String())
    phonc = sa.Column("phonc", sa.Integer(), default=0)
    is_phone_number_confirmed = column_property(
        case((phonc == 1, True), else_=False)
    )
    tface = sa.Column("tface", sa.Integer(), default=0)
    two_factor_enabled = column_property(
        case((tface == 1, True), else_=False)
    )
    locen = sa.Column("locen", sa.Integer(), default=0)  # TODO: change to boolean
    lock_enabled = column_property(
        case((locen == 1, True), else_=False)
    )
    valid_until = sa.Column("loced", sa.DateTime())
    acfct = sa.Column("acfct", sa.Integer())
    remme = sa.Column("remme", sa.Integer(), default=0)  # TODO: change to boolean
    remember_me = column_property(
        case((remme == 1, True), else_=False)
    )
    first_approver_id = sa.Column("ldid1", sa.String())
    second_approver_id = sa.Column("ldid2", sa.String())
    third_approver_id = sa.Column("ldid3", sa.String())
    flag1 = sa.Column("flag1", sa.String(15))
    flag2 = sa.Column("flag2", sa.String(15))
    reference_id = sa.Column("stats", sa.Integer(), sa.ForeignKey("references.id"))
    temps = sa.Column("temps", sa.String(100))

    isact = sa.Column("isact", sa.Integer(), default=0)  # TODO: change to boolean
    is_active = column_property(
        case((isact == 1, True), else_=False)
    )

    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
