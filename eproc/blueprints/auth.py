from flask import Blueprint
from flask_restful import Api

from eproc.resources.auth.role import RoleResource
from eproc.resources.auth.user_role import UserRoleResource
from eproc.resources.auth.user_role_menu import UserRoleMenuResource
from eproc.resources.auth.register import RegisterResource
from eproc.resources.auth.login import LoginResource
from eproc.resources.auth.login import LoginResource
from eproc.resources.auth.menu import (
    MenuResource,
    MenuDetailResource,
)

auth_blueprint = Blueprint("auth_blueprint", __name__, url_prefix="/auth")

auth_api = Api(auth_blueprint)

auth_api.add_resource(RegisterResource, "/register")
auth_api.add_resource(LoginResource, "/login")
auth_api.add_resource(RoleResource, "/role")
auth_api.add_resource(UserRoleResource, "/user-role")
auth_api.add_resource(MenuResource, "/menu")
auth_api.add_resource(MenuDetailResource, "/menu/detail")
auth_api.add_resource(UserRoleMenuResource, "/user-role-info")
