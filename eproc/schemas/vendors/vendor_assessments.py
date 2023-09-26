from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.vendors.vendor_assessments import VendorAssessment


class VendorAssessmentAutoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VendorAssessment
        load_instance = True
        ordered = True
        unknown = EXCLUDE
