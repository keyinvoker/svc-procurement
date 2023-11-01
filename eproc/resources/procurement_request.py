from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.procurement_request import ProcurementRequestController
from eproc.helpers.commons import split_string_into_list
from eproc.schemas.procurement_requests import (
    ProcurementRequestGetInputSchema,
    ProcurementRequestDetailGetInputSchema,
    ProcurementRequestPostInputSchema,
)
from eproc.tools.response import make_json_response
from eproc.tools.validation import schema_validate_and_load


class ProcurementRequestResource(Resource):
    def __init__(self):
        self.controller = ProcurementRequestController()

    def get(self) -> Response:
        try:
            list_param_keys = [
                "id_list",
            ]
            input_data = split_string_into_list(
                request.args.to_dict(),
                list_param_keys
            )
            schema = ProcurementRequestGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            (
                http_status, message, data_list, total
            ) = self.controller.get_list(**payload)

            data = dict(
                data=data_list,
                total=total,
                limit=payload["limit"],
                offset=payload["offset"],
            )

            return make_json_response(
                http_status=http_status,
                message=message,
                data=data,
            )
        except Exception as e:
            error_logger.error(f"Error on Procurement Request [GET] :: {e}, {format_exc()}")
            return make_json_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        
    def post(self):
        try:
            return HTTPStatus.OK, "", request.get_json()
            input_data = request.get_json()

            schema = ProcurementRequestPostInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            from eproc import app_logger
            app_logger.info(f"Procurement Request [POST] :: payload: {payload}")

            http_status, message = self.controller.create(**payload)

            return make_json_response(
                http_status=http_status,
                message=message,
                data=payload
            )
        except Exception as e:
            error_logger.error(f"Error on Procurement Request [POST] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class ProcurementRequestDetailResource(Resource):
    def __init__(self):
        self.controller = ProcurementRequestController()

    def get(self) -> Response:
        try:
            schema = ProcurementRequestDetailGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=request.args.to_dict(),
            )
            if not is_valid:
                return response

            (
                http_status, message, data
            ) = self.controller.get_detail(payload["id"])

            return make_json_response(
                http_status=http_status,
                message=message,
                data=data
            )
        except Exception as e:
            error_logger.error(f"Error on Procurement Request Detail [GET] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
