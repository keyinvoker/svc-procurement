from flask import Blueprint
from flask_restful import Api

from eproc.resources.procurement_request_progress import (
    ProcurementRequestProgressResource
)

procurement_request_progress_blueprint = Blueprint("procurement_request_progress_blueprint", __name__, url_prefix="/pr-progress")
procurement_request_progress_api = Api(procurement_request_progress_blueprint)

procurement_request_progress_api.add_resource(ProcurementRequestProgressResource, "")
