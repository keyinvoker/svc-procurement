from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.auth.menu import MenuController
from eproc.helpers.commons import split_string_into_list
from eproc.schemas.auth.menus import (
    MenuGetInputSchema,
    MenuDetailGetInputSchema,
)
from eproc.tools.decorator import validate_token
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class MenuResource(Resource):
    @validate_token
    def get(self) -> Response:
        try:
            list_param_keys = [
                "id_list",
            ]
            input_data = split_string_into_list(
                request.args.to_dict(),
                list_param_keys
            )
            schema = MenuGetInputSchema()
            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            (
                http_status, message, data, total
            ) = MenuController().get_list(**payload)

            data = dict(
                data=data,
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
            error_logger.error(f"Error on Menu [GET] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class MenuDetailResource(Resource):
    @validate_token
    def get(self) -> Response:
        try:
            schema = MenuDetailGetInputSchema()
            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=request.args.to_dict(),
            )
            if not is_valid:
                return response

            (
                http_status, message, data
            ) = MenuController().get_detail(**payload)

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=dict(data=data)
            )
        except Exception as e:
            error_logger.error(f"Error on MenuDetail [GET] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
