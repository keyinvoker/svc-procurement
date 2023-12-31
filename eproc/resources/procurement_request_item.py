from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.procurement_request import ProcurementRequestController
from eproc.tools.decorator import validate_token
from eproc.schemas.items.procurement_request_items import (
    ProcurementRequesItemGetInputSchema
)
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class ProcurementRequestItemResource(Resource):
    def __init__(self):
        self.controller = ProcurementRequestController()
    
    @validate_token
    def get(self) -> Response:
        try:
            schema = ProcurementRequesItemGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=request.args.to_dict(),
            )
            if not is_valid:
                return response

            (
                http_status, message, data, total
            ) = self.controller.get_items(**payload)

            data = dict(
                data=data,
                total=total,
                limit=payload["limit"],
                offset=payload["offset"],
            )

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=data,
            )
        except Exception as e:
            error_logger.error(f"Error on PR Item [GET] :: {e}, {format_exc()}")
            return construct_api_response(HTTPStatus.INTERNAL_SERVER_ERROR)
