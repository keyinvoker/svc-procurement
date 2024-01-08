from flask import Blueprint
from flask_restful import Api

from eproc.resources.procurement_request import (
    ProcurementRequestResource,
    ProcurementRequestDetailResource,
)
from eproc.resources.procurement_request_item import ProcurementRequestItemResource

procurement_request_blueprint = Blueprint("procurement_request_blueprint", __name__, url_prefix="/procurement-request")

procurement_request_api = Api(procurement_request_blueprint)

procurement_request_api.add_resource(ProcurementRequestResource, "")
procurement_request_api.add_resource(ProcurementRequestDetailResource, "/details")
procurement_request_api.add_resource(ProcurementRequestItemResource, "/items")
