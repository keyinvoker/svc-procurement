from flask import Response, g, request
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
from eproc.tools.decorator import validate_token
from eproc.tools.response import construct_api_response
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

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=data,
            )
        except Exception as e:
            error_logger.error(f"Error on Procurement Request [GET] :: {e}, {format_exc()}")
            return construct_api_response(HTTPStatus.INTERNAL_SERVER_ERROR)

    @validate_token
    def post(self):
        try:
            input_data = request.get_json()

            schema = ProcurementRequestPostInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response
            
            payload["preparer_id"] = g.user_id

            http_status, message, data = self.controller.create(**payload)

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=data,
            )
        except Exception as e:
            error_logger.error(f"Error on Procurement Request [POST] :: {e}, {format_exc()}")
            return construct_api_response(
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

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=data
            )
        except Exception as e:
            error_logger.error(f"Error on Procurement Request Detail [GET] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
