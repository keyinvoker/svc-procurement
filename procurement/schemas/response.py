from datetime import datetime
from marshmallow import Schema, fields


class BaseResponseSchema(Schema):
    code = fields.Integer()
    message = fields.String()
    timestamp = fields.DateTime(default=datetime.utcnow())

    class Meta:
        ordered = True


class BaseErrorResponseSchema(BaseResponseSchema):
    errors = fields.Raw()


class DefaultResponseSchema(BaseResponseSchema):
    data = fields.Dict(default=dict())


class DefaultStringResponseSchema(BaseResponseSchema):
    data = fields.Raw()
