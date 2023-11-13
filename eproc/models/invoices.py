import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel, WIBNow
from eproc.helpers.commons import wibnow


class Invoice(BaseModel):
    __tablename__ = "invoices"

    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True)
    purchase_order_id = sa.Column(sa.BigInteger(), sa.ForeignKey("purchase_orders.id"))
    vendor_id = sa.Column(sa.String(100), sa.ForeignKey("vendors.id"), nullable=False)
    cost_center_id = sa.Column(sa.String(20), sa.ForeignKey("cost_centers.id"))
    reference_id = sa.Column(sa.Integer(), sa.ForeignKey("references.id"), nullable=False, default=0, server_default="0")
    transaction_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    year = sa.Column(sa.Integer(), nullable=False)
    month = sa.Column(sa.Integer(), nullable=False)
    invoice_date = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    invoice_number = sa.Column(sa.String(50))
    invoice_amount = sa.Column(sa.Numeric(38, 2), nullable=False, default=0.00, server_default="0.00")
    termin = sa.Column(sa.Integer(), nullable=False)
    document_number = sa.Column(sa.String(20))
    app_source = sa.Column(sa.String(20), default="epro", server_default="epro")
    description = sa.Column(sa.String(500))
    image_path = sa.Column(sa.String(10485760))
    tax_percentage = sa.Column(sa.Numeric(38, 2), nullable=False, default=0.00, server_default="0.00")

    sequence_number = sa.Column(sa.Integer(), nullable=False)
    dref1 = sa.Column(sa.String(100))
    dref2 = sa.Column(sa.String(100))
    dref3 = sa.Column(sa.String(100))
    flag1 = sa.Column(sa.String(15))
    flag2 = sa.Column(sa.String(15))
    temps = sa.Column(sa.String(100))

    purchase_orders = db.relationship(
        "PurchaseOrder", backref=backref(__tablename__, uselist=False)
    )
    vendor = db.relationship(
        "Vendor", backref=backref(__tablename__, uselist=False)
    )
    cost_center = db.relationship(
        "CostCenter", backref=backref(__tablename__, uselist=False)
    )
    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )

