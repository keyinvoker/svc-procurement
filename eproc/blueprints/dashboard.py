from flask import Blueprint
from flask_restful import Api

from eproc.resources.dashboard import DashboardResource

dashboard_blueprint = Blueprint("dashboard_blueprint", __name__, url_prefix="/dashboard")

dashboard_api = Api(dashboard_blueprint)

dashboard_api.add_resource(DashboardResource, "")
