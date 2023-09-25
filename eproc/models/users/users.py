import sqlalchemy as sa
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = sa.Column("usrid", sa.String(), primary_key=True)
    app_id = sa.Column("appid", sa.String(), default=None)
    username = sa.Column("uname", sa.String(), default=None)  # TODO: delete later, because literally same as `usrid`
    full_name = sa.Column("ffnam", sa.String(), default=None)
    password = sa.Column("paswd", sa.String(), default=None)
    password_length = sa.Column("pasfm", sa.Integer(), default=None)  # TODO DELETE: why store password_length in db ???
    passt = sa.Column("passt", sa.String(), default=None)
    password_hash = sa.Column("pashs", sa.String(), default=None)
    pasqs = sa.Column("pasqs", sa.String(), default=None)
    pasaw = sa.Column("pasaw", sa.String(), default=None)
    secst = sa.Column("secst", sa.String(10), default=None)
    email = sa.Column("email", sa.String(), default=None)
    emcon = sa.Column("emcon", sa.Integer(), default=0)  # TODO: change to boolean
    isann = sa.Column("isann", sa.Integer(), default=0)  # TODO: change to boolean
    is_admin = sa.Column("isadm", sa.Integer(), default=0)  # TODO: change to boolean
    isuho = sa.Column("isuho", sa.Integer(), default=1)  # TODO: change to boolean
    isukp = sa.Column("isukp", sa.Integer(), default=0)  # TODO: change to boolean
    isust = sa.Column("isust", sa.Integer(), default=0)  # TODO: change to boolean
    isapr = sa.Column("isapr", sa.Integer(), default=0)  # TODO: change to boolean
    is_approved = column_property(case(
        (isapr == 1, True), else_=False
    ))
    is_locked = sa.Column("islck", sa.Integer(), default=0)  # TODO: change to boolean
    sapsa = sa.Column("sapsa", sa.String(6), default=None)
    mopin = sa.Column("mopin", sa.String(16), default=None)
    moals = sa.Column("moals", sa.String(16), default=None)
    ladat = sa.Column("ladat", sa.DateTime(), default=None)
    last_login_at = sa.Column("llgdt", sa.DateTime(), default=None)
    llkdt = sa.Column("llkdt", sa.DateTime(), default=None)
    lpcdt = sa.Column("lpcdt", sa.DateTime(), default=None)  # last procurement date?
    comment = sa.Column("comnt", sa.String(), default=None)
    phone_number = sa.Column("phono", sa.String(), default=None)
    phonc = sa.Column("phonc", sa.Integer(), default=0)  # TODO: change to boolean
    tface = sa.Column("tface", sa.Integer(), default=0)  # TODO: change to boolean
    locen = sa.Column("locen", sa.Integer(), default=0)  # TODO: change to boolean
    loced = sa.Column("loced", sa.DateTime(), default=None)
    acfct = sa.Column("acfct", sa.Integer(), default=None)
    remme = sa.Column("remme", sa.Integer(), default=0)  # TODO: change to boolean
    first_approver_id = sa.Column("ldid1", sa.String(), default=None)
    second_approver_id = sa.Column("ldid2", sa.String(), default=None)
    third_approver_id = sa.Column("ldid3", sa.String(), default=None)
    flag1 = sa.Column("flag1", sa.String(15), default=None)
    flag2 = sa.Column("flag2", sa.String(15), default=None)
    stats = sa.Column("stats", sa.Integer(), default=None)  # TODO: has to be a Foreign Key to another table that contains the string values
    temps = sa.Column("temps", sa.String(100), default=None)

    isact = sa.Column("isact", sa.Integer(), default=0)  # TODO: change to boolean
    is_active = column_property(
        case((isact == 1, True), else_=False)
    )

    # region: TODO: NEW
    # role_id = sa.Column(
    #     sa.BigInteger,
    #     sa.ForeignKey("roles.id"),
    #     nullable=True
    # )
    
    # employee_identification_number = sa.Column(sa.String(255), nullable=False)

    # password_updated_at = sa.Column(sa.DateTime(), default=None)

    # role = db.relationship(
    #     "Role", backref=backref(__tablename__, uselist=False)
    # )
    # endregion
