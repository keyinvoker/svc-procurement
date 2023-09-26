from marshmallow import EXCLUDE, Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.users.users import User
from eproc.schemas.references import ReferenceAutoSchema


class UserAutoSchema(SQLAlchemyAutoSchema):
    first_approve_full_name = fields.String()
    status = fields.String()

    class Meta:
        model = User
        load_instance = True
        ordered = True
        unknown = EXCLUDE


class UserGetInputSchema(Schema):
    id_list = fields.List(
        fields.Integer(),
        dump_default=[],
        load_default=[],
    )
    search_query = fields.String(
        allow_none=True,
        dump_default="",
        load_default="",
    )
    limit = fields.Integer(
        allow_none=True,
        dump_default=None,
        load_default=None,
    )
    offset = fields.Integer(
        allow_none=True,
        dump_default=0,
        load_default=0,
    )

    class Meta:
        ordered = True
        unknown = EXCLUDE


class UserDetailGetInputSchema(Schema):
    id = fields.String(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
