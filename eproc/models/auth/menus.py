import sqlalchemy as sa

from eproc.models.base_model import BaseModel


class Menu(BaseModel):
    __tablename__ = "menus"

    id = sa.Column(sa.String(12), primary_key=True)
    app_id = sa.Column(sa.String(10), nullable=False)
    module_id = sa.Column(sa.String(10), nullable=False)
    menu_name = sa.Column(sa.String(100))
    menu_tag = sa.Column(sa.String(100))
    level = sa.Column(sa.Integer(), nullable=False)
    prnid = sa.Column("prnid", sa.String(10))
    clasz = sa.Column("clasz", sa.String(20))
    cntlr = sa.Column("cntlr", sa.String(20))
    action = sa.Column(sa.String(50))
    action_url = sa.Column(sa.String(50))
    icon = sa.Column(sa.String(20))
    lstid = sa.Column("lstid", sa.String(20))
    regfl = sa.Column("regfl", sa.String(100))
    appfl = sa.Column("appfl", sa.String(100))
    rejfl = sa.Column("rejfl", sa.String(100))
    appif = sa.Column("appif", sa.Boolean(), nullable=False)
    isprn = sa.Column("isprn", sa.Boolean(), nullable=False)
    sqenc = sa.Column("sqenc", sa.Integer(), nullable=False)
    is_active = sa.Column(sa.Boolean(), nullable=False, default=True, server_default="true")
