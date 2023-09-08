import sqlalchemy as sa

from procurement.models.base_model import BaseModel


class LoginParameter(BaseModel):
    __tablename__ = "login_parameters"

    password_expiration_days = sa.Column(sa.Integer(), default=61)
    minimumm_password_length = sa.Column(sa.Integer(), default=8)
    password_recycle_count = sa.Column(sa.Integer(), default=3)
    lockout_threshold_days = sa.Column(sa.Integer(), default=183)
    max_password_attempts = sa.Column(sa.Integer(), default=3)
