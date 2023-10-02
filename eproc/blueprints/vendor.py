from flask import Blueprint
from flask_restful import Api

from eproc.resources.vendor.vendor import (
    VendorDetailResource,
    VendorResource
)

vendor_blueprint = Blueprint("vendor_blueprint", __name__, url_prefix="/vendor")

vendor_api = Api(vendor_blueprint)

vendor_api.add_resource(VendorResource, "")
vendor_api.add_resource(VendorDetailResource, "/details")
