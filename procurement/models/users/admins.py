from procurement import db
from procurement.models.base_model import BaseModel


class Admin(BaseModel):
    __tablename__ = "admins"

    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.ForeignKey("roles", backref=__tablename__)
