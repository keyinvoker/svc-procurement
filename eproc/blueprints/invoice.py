from flask import Blueprint
from flask_restful import Api

from eproc.resources.invoice import (
    InvoiceResource,
    InvoiceDetailResource,
    InvoiceTerminResource,
)

invoice_blueprint = Blueprint("invoice_blueprint", __name__, url_prefix="/invoice")
invoice_api = Api(invoice_blueprint)
invoice_api.add_resource(InvoiceResource, "")
invoice_api.add_resource(InvoiceDetailResource, "/details")
invoice_api.add_resource(InvoiceTerminResource, "/next-termin")
