from marshmallow import Schema, fields

from eproc.helpers.commons import wibnow


class DefaultResponseSchema(Schema):
    status = fields.Integer()
    message = fields.String()
    timestamp = fields.DateTime(default=wibnow())
    data = fields.Dict(default=dict())

    class Meta:
        ordered = True
