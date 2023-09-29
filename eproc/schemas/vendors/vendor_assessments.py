from marshmallow import EXCLUDE, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.vendors.vendor_assessments import VendorAssessment
from eproc.schemas.references import ReferenceAutoSchema
from eproc.schemas.users.users import UserAutoSchema
from eproc.schemas.vendors.vendors import VendorAutoSchema


class VendorAssessmentAutoSchema(SQLAlchemyAutoSchema):
    vendor = fields.Nested(VendorAutoSchema)
    assessor = fields.Nested(UserAutoSchema)
    reference = fields.Nested(ReferenceAutoSchema)

    class Meta:
        model = VendorAssessment
        load_instance = True
        ordered = True
        unknown = EXCLUDE
