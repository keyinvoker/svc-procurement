import sqlalchemy as sa

from eproc.helpers.commons import wibnow
from eproc.models.base_model import BaseModel, WIBNow


class UserToken(BaseModel):
    __tablename__ = "user_tokens"

    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.String(24), nullable=False)
    auth_token = sa.Column(sa.String(255), nullable=False)
    expires_at = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    is_active = sa.Column(sa.Boolean(), nullable=False, default=True, server_default="true")
