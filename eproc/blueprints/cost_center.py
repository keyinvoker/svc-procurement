from flask import Blueprint
from flask_restful import Api

from eproc.resources.cost_center import CostCenterResource

cost_center_blueprint = Blueprint( "cost_center_blueprint", __name__, url_prefix="/cost-center")
cost_center_api = Api(cost_center_blueprint)
cost_center_api.add_resource(CostCenterResource, "")
