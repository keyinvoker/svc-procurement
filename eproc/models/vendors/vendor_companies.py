import sqlalchemy as sa
from sqlalchemy.orm import backref

from eproc import db
from eproc.models.base_model import BaseModel


class VendorCompany(BaseModel):
    __tablename__ = "vendor_companies"
