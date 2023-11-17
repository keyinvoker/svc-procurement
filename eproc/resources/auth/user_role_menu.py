from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.helpers.auth import get_user_role_info
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class UserRoleMenuResource(Resource):
    def get(self) -> Response:
        try:
            input_data = request.args.to_dict()
            if "user_id" not in input_data:
                return construct_api_response(
                    HTTPStatus.BAD_REQUEST,
                    "Tolong masukkan user id."
                )

            data = get_user_role_info(input_data["user_id"])
            if not data:
                return construct_api_response(
                    http_status=HTTPStatus.NOT_FOUND,
                    message="Info user role tidak ada."
                )

            return construct_api_response(
                http_status=HTTPStatus.OK,
                message="Info user role berhasil diambil.",
                data=data
            )
        except Exception as e:
            error_logger.error(f"Error on User Role Menu [GET] :: {e}, {format_exc()}")