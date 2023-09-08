import sqlalchemy as sa
from sqlalchemy.orm import backref

from procurement import db
from procurement.models.base_model import BaseModel


class VendorCompany(BaseModel):
    __tablename__ = "vendor_companies"
