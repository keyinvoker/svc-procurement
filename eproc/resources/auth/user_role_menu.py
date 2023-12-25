from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.helpers.auth import get_user_role_info
from eproc.schemas.auth.users_roles_menus import UserRoleMenuSchema
from eproc.tools.decorator import validate_token
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class UserRoleMenuResource(Resource):
    @validate_token
    def get(self) -> Response:
        try:
            is_valid, response, payload = schema_validate_and_load(
                payload=request.args.to_dict(),
                schema=UserRoleMenuSchema()
            )
            if not is_valid:
                return response

            data = get_user_role_info(payload["user_id"])
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
