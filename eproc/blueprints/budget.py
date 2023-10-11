from flask import Blueprint
from flask_restful import Api

from eproc.resources.budget import BudgetResource

budget_blueprint = Blueprint("budget_blueprint", __name__, url_prefix="/budget")

budget_api = Api(budget_blueprint)

budget_api.add_resource(BudgetResource, "")
