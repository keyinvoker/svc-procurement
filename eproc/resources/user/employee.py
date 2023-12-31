from flask import Response, g, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.employee import EmployeeController
from eproc.helpers.commons import split_string_into_list
from eproc.schemas.users.employees import (
    EmployeeDetailGetInputSchema,
    EmployeeGetInputSchema,
)
from eproc.tools.decorator import validate_token
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class EmployeeResource(Resource):
    @validate_token
    def get(self):
        try:
            list_param_keys = [
                "id_list",
            ]
            input_data = split_string_into_list(
                request.args.to_dict(),
                list_param_keys
            )
            schema = EmployeeGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            (
                http_status, message, data_list, total
            ) = EmployeeController().get_list(**payload)

            data = dict(
                data=data_list,
                total=total,
                limit=payload["limit"],
                offset=payload["offset"],
            )

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=data
            )
        except Exception as e:
            error_logger.error(f"Error on Employee [GET] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class EmployeeDetailResource(Resource):
    @validate_token
    def get(self) -> Response:
        try:
            schema = EmployeeDetailGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=request.args.to_dict(),
            )
            if not is_valid:
                return response

            (
                http_status, message, data
            ) = EmployeeController().get_detail(payload["id"])

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=data
            )
        except Exception as e:
            error_logger.error(f"Error on Employee Detail [GET] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
