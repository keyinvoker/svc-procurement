from flask import Blueprint
from flask_restful import Api

from eproc.resources.purchase_order import (
    PurchaseOrderResource,
    PurchaseOrderDetailResource,
    PurchaseOrderItemResource,
)

purchase_order_blueprint = Blueprint("purchase_order_blueprint", __name__, url_prefix="/purchase-order")

purchase_order_api = Api(purchase_order_blueprint)

purchase_order_api.add_resource(PurchaseOrderResource, "")
purchase_order_api.add_resource(PurchaseOrderDetailResource, "/details")
purchase_order_api.add_resource(PurchaseOrderItemResource, "/items")
