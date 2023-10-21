from flask import Blueprint
from flask_restful import Api

from eproc.resources.system_config import SystemConfigResource

system_config_blueprint = Blueprint("system_config_blueprint", __name__, url_prefix="/system-config")
system_config_api = Api(system_config_blueprint)
system_config_api.add_resource(SystemConfigResource, "")
