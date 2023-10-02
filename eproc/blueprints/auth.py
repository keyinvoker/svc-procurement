from flask import Blueprint
from flask_restful import Api

from eproc.resources.auth.role import RoleResource
from eproc.resources.auth.register import RegisterResource
from eproc.resources.auth.login import LoginResource

auth_blueprint = Blueprint("auth_blueprint", __name__, url_prefix="/auth")

auth_api = Api(auth_blueprint)

auth_api.add_resource(RegisterResource, "/register")
auth_api.add_resource(LoginResource, "/login")
auth_api.add_resource(RoleResource, "/role")
