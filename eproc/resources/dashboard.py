from flask import Response
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.dashboard import DashboardController
from eproc.tools.response import construct_api_response


class DashboardResource(Resource):
    def __init__(self):
        self.controller = DashboardController()

    def get(self) -> Response:
        try:
            data = dict(
                active_vendor_count=self.controller.get_active_vendor_count(),
                pending_vendor_count=self.controller.get_pending_vendor_count(),
                pending_rfq_count=self.controller.get_pending_rfq_count(),
                pending_vendor_price_count=self.controller.get_pending_vendor_price_count(),
            )
            return construct_api_response(
                http_status=HTTPStatus.OK,
                data=data,
            )
        except Exception as e:
            error_logger.error(f"Error on Dashboard [GET] :: {e}, {format_exc()}")
            return construct_api_response(HTTPStatus.INTERNAL_SERVER_ERROR)
