from flask import Blueprint
from flask_restful import Api

from eproc.resources.rfq import (
    RFQResource,
    RFQDetailResource,
)

rfq_blueprint = Blueprint("rfq_blueprint", __name__, url_prefix="/rfq")
rfq_api = Api(rfq_blueprint)
rfq_api.add_resource(RFQResource, "")
rfq_api.add_resource(RFQDetailResource, "/detail")
