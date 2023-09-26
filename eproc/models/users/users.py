import sqlalchemy as sa
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = sa.Column(sa.String(), primary_key=True)
    app_id = sa.Column("appid", sa.String(), default=None)
    username = sa.Column("uname", sa.String(), default=None)  # TODO: delete later, because literally same as `usrid`
    full_name = sa.Column("ffnam", sa.String(), default=None)
    password = sa.Column("paswd", sa.String(), default=None)
    password_length = sa.Column("pasfm", sa.Integer(), default=None)
    password_salt = sa.Column("passt", sa.String(), default=None)
    password_hash = sa.Column("pashs", sa.String(), default=None)
    password_question = sa.Column("pasqs", sa.String(), default=None)
    password_answer = sa.Column("pasaw", sa.String(), default=None)
    security_status = sa.Column("secst", sa.String(10), default=None)
    email = sa.Column("email", sa.String(), default=None)
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
    captcha = sa.Column("sapsa", sa.String(6), default=None)  # TODO: idk wtf for ???
    mobile_pin = sa.Column("mopin", sa.String(16), default=None)
    mobile_alias = sa.Column("moals", sa.String(16), default=None)
    last_active_date = sa.Column("ladat", sa.DateTime(), default=None)
    last_login_date = sa.Column("llgdt", sa.DateTime(), default=None)
    last_lock_date = sa.Column("llkdt", sa.DateTime(), default=None)
    last_change_date = sa.Column("lpcdt", sa.DateTime(), default=None)  # last procurement date?
    comment = sa.Column("comnt", sa.String(), default=None)
    phone_number = sa.Column("phono", sa.String(), default=None)
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
    valid_until = sa.Column("loced", sa.DateTime(), default=None)
    acfct = sa.Column("acfct", sa.Integer(), default=None)
    remme = sa.Column("remme", sa.Integer(), default=0)  # TODO: change to boolean
    remember_me = column_property(
        case((remme == 1, True), else_=False)
    )
    first_approver_id = sa.Column("ldid1", sa.String(), default=None)
    second_approver_id = sa.Column("ldid2", sa.String(), default=None)
    third_approver_id = sa.Column("ldid3", sa.String(), default=None)
    flag1 = sa.Column("flag1", sa.String(15), default=None)
    flag2 = sa.Column("flag2", sa.String(15), default=None)
    reference_id = sa.Column("stats", sa.Integer(), sa.ForeignKey("references.id"))
    temps = sa.Column("temps", sa.String(100), default=None)

    isact = sa.Column("isact", sa.Integer(), default=0)  # TODO: change to boolean
    is_active = column_property(
        case((isact == 1, True), else_=False)
    )

    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
