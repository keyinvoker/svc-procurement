from flask import Blueprint
from flask_restful import Api

from eproc.resources.user import (
    EmployeeResource,
    EmployeeDetailResource,
    UserResource,
    UserDetailResource,
)

user_blueprint = Blueprint("user_blueprint", __name__, url_prefix="/user")

user_api = Api(user_blueprint)

user_api.add_resource(UserResource, "")
user_api.add_resource(UserDetailResource, "/details")


employee_blueprint = Blueprint("employee_blueprint", __name__, url_prefix="/employee")

employee_api = Api(employee_blueprint)

employee_api.add_resource(EmployeeResource, "")
employee_api.add_resource(EmployeeDetailResource, "/details")
