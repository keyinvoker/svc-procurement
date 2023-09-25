from flask import Blueprint
from flask_restful import Api

from eproc.resources.user import (
    UserResource,
    UserDetailResource,
)

user_blueprint = Blueprint("user_blueprint", __name__, url_prefix="/vendor")
user_api = Api(user_blueprint)

user_api.add_resource(UserResource, "")
user_api.add_resource(UserDetailResource, "/detail")
