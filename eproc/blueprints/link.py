from flask import Blueprint
from flask_restful import Api

from eproc.resources.link import LinkResource

link_blueprint = Blueprint("link_blueprint", __name__, url_prefix="/link")
link_api = Api(link_blueprint)
link_api.add_resource(LinkResource, "")
