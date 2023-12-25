from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.auth.user_role import UserRoleController
from eproc.schemas.auth.users_roles import UserRoleGetInputSchema
from eproc.tools.decorator import validate_token
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class UserRoleResource(Resource):
    @validate_token
    def get(self) -> Response:
        try:
            schema = UserRoleGetInputSchema()
            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=request.args.to_dict(),
            )
            if not is_valid:
                return response

            (
                http_status, message, data, total
            ) = UserRoleController().get_list(**payload)

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=dict(data=data, total=total)
            )
        except Exception as e:
            error_logger.error(f"Error on User Roles [GET] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
