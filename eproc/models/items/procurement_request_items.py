import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.helpers.commons import wibnow
from eproc.models.base_model import BaseModel, WIBNow


class ProcurementRequestItem(BaseModel):
    __tablename__ = "procurement_request_items"

    line_number = sa.Column(sa.Integer(), nullable=False, primary_key=True, autoincrement=True)
    procurement_request_id = sa.Column(sa.BigInteger(), sa.ForeignKey("procurement_requests.id"), nullable=False, primary_key=True)
    item_id = sa.Column(sa.String(20), sa.ForeignKey("items.id"), nullable=False)
    currency_id = sa.Column(sa.String(20), sa.ForeignKey("currencies.id"), nullable=False)
    unit_of_measurement = sa.Column(sa.String(20), nullable=False)
    quantity = sa.Column(sa.Numeric(18, 2), nullable=False)

    # TODO: field names
    aprqt = sa.Column("aprqt", sa.Numeric(18, 2), nullable=False)
    esprc = sa.Column("esprc", sa.Numeric(22, 2), nullable=False, default=0, server_default="0")
    required_days_interval = sa.Column(sa.Integer(), nullable=False)
    required_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    notes = sa.Column(sa.String(500))

    ktuck = sa.Column("ktuck", sa.Integer())
    gmkck = sa.Column("gmkck", sa.Integer())
    uhock = sa.Column("uhock", sa.Integer())
    ghock = sa.Column("ghock", sa.Integer())
    budck = sa.Column("budck", sa.Integer())
    bcchk = sa.Column("bcchk", sa.Integer())
    mdchk = sa.Column("mdchk", sa.Integer())
    rdcrt = sa.Column("rdcrt", sa.Integer())
    odrop = sa.Column("odrop", sa.Integer())
    aloct = sa.Column("aloct", sa.Integer())
    ipath = sa.Column("ipath", sa.String(10485760))
    # pictr = sa.Column("pictr", sa.String())
    picty = sa.Column("picty", sa.String(200))
    picfn = sa.Column("picfn", sa.String(200))
    picsz = sa.Column("picsz", sa.Numeric(22, 2), nullable=False, default=0, server_default="0")

    procurement_request = db.relationship(
        "ProcurementRequest", backref=backref(__tablename__, uselist=False)
    )
    item = db.relationship(
        "Item", backref=backref(__tablename__, uselist=False)
    )
    currency = db.relationship(
        "Currency", backref=backref(__tablename__, uselist=False)
    )  # TODO: currency table 
