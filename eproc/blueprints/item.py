from flask import Blueprint
from flask_restful import Api

from eproc.resources.item import (
    ItemResource,
    ItemCategoryResource,
)

item_blueprint = Blueprint("item_blueprint", __name__, url_prefix="/item")
item_api = Api(item_blueprint)
item_api.add_resource(ItemResource, "")
item_api.add_resource(ItemCategoryResource, "/category")
