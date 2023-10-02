from flask import Blueprint
from flask_restful import Api

from eproc.resources.company.branch import BranchResource
from eproc.resources.company.directorate import DirectorateResource
from eproc.resources.company.division import DivisionResource
from eproc.resources.company.department import DepartmentResource

company_blueprint = Blueprint("company_blueprint", __name__, url_prefix="/company")

company_api = Api(company_blueprint)

company_api.add_resource(BranchResource, "/branch")
company_api.add_resource(DirectorateResource, "/directorate")
company_api.add_resource(DivisionResource, "/division")
company_api.add_resource(DepartmentResource, "/department")
