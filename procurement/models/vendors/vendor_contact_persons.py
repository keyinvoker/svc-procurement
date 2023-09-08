import sqlalchemy as sa

from procurement.models.base_model import BaseModel


class VendorContactPerson(BaseModel):
    __tablename__ = "vendor_contact_persons"

    name = sa.Column(sa.String(255), nullable=False)
    designation = sa.Column(sa.String(255), nullable=False)
    phone_number = sa.Column(sa.String(255), nullable=False)
    email = sa.Column(sa.String(255), nullable=False)
