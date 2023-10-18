from flask import Blueprint
from flask_restful import Api

from eproc.resources.user.employee import (
    EmployeeResource,
    EmployeeDetailResource,
)

employee_blueprint = Blueprint("employee_blueprint", __name__, url_prefix="/employee")
employee_api = Api(employee_blueprint)
employee_api.add_resource(EmployeeResource, "")
employee_api.add_resource(EmployeeDetailResource, "/details")
