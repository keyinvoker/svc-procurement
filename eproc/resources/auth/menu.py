from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.auth.menu import MenuController
from eproc.schemas.auth.menus import MenuGetInputSchema
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class MenuResource(Resource):
    def get(self) -> Response:
        try:
            schema = MenuGetInputSchema()
            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=request.args.to_dict(),
            )
            if not is_valid:
                return response

            (
                http_status, message, data, total
            ) = MenuController().get_list(**payload)

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=dict(data=data, total=total)
            )
        except Exception as e:
            error_logger.error(f"Error on Menu [GET] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
