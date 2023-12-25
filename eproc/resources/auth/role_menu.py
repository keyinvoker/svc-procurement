from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.auth.role_menu import RoleMenuController
from eproc.helpers.commons import split_string_into_list
from eproc.schemas.auth.roles_menus import RoleMenuGetInputSchema
from eproc.tools.decorator import validate_token
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class RoleMenuResource(Resource):
    @validate_token
    def get(self) -> Response:
        try:
            list_param_keys = [
                "role_id_list",
                "menu_id_list",
            ]
            input_data = split_string_into_list(
                request.args.to_dict(),
                list_param_keys
            )
            schema = RoleMenuGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                print(payload)
                return response

            (
                http_status, message, data, total
            ) = RoleMenuController().get_list(**payload)

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=dict(data=data, total=total)
            )
        except Exception as e:
            error_logger.error(f"Error on RoleMenu [GET] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
