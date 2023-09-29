from flask import Blueprint
from flask_restful import Api

from eproc.resources.vendor_rfq import (
    VendorRFQResource
)

vendor_rfq_blueprint = Blueprint("vendor_rfq_blueprint", __name__, url_prefix="/vendor-rfq")

vendor_rfq_api = Api(vendor_rfq_blueprint)

vendor_rfq_api.add_resource(VendorRFQResource, "")
