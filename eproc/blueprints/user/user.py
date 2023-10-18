from flask import Blueprint
from flask_restful import Api

from eproc.resources.user.user import (
    UserResource,
    UserDetailResource,
    UserProfileResource,
    UserResetPasswordResource,
    UserUnlockResource,
)

user_blueprint = Blueprint("user_blueprint", __name__, url_prefix="/user")
user_api = Api(user_blueprint)
user_api.add_resource(UserResource, "")
user_api.add_resource(UserDetailResource, "/details")
user_api.add_resource(UserResetPasswordResource, "/reset-password")
user_api.add_resource(UserUnlockResource, "/unlock")
user_api.add_resource(UserProfileResource, "/profile")
