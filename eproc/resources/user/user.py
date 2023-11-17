from flask import Response, g, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.user import UserController
from eproc.helpers.commons import split_string_into_list
from eproc.schemas.users.users import (
    UserDetailGetInputSchema,
    UserGetInputSchema,
    UserPostInputSchema,
    UserResetPasswordInputSchema,
    UserUnlockInputSchema,
)
from eproc.tools.decorator import validate_token
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class UserResource(Resource):
    def get(self) -> Response:
        try:
            list_param_keys = [
                "id_list",
            ]
            input_data = split_string_into_list(
                request.args.to_dict(),
                list_param_keys
            )
            schema = UserGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            (
                http_status, message, data_list, total
            ) = UserController().get_list(**payload)

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
            error_logger.error(f"Error on User [GET] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
        
    def post(self) -> Response:
        try:
            input_data = request.get_json()
            schema = UserPostInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            from eproc import app_logger
            app_logger.info(f"User [POST] :: payload: {payload}")

            http_status, message = UserController().register_user(**payload)

            return construct_api_response(
                http_status=http_status,
                message=message,
            )
        except Exception as e:
            error_logger.error(f"Error on User [POST] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class UserDetailResource(Resource):
    def get(self) -> Response:
        try:
            schema = UserDetailGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=request.args.to_dict(),
            )
            if not is_valid:
                return response

            (
                http_status, message, data
            ) = UserController().get_detail(payload["id"])

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=data
            )
        except Exception as e:
            error_logger.error(f"Error on User Detail [GET] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class UserProfileResource(Resource):
    @validate_token
    def get(self) -> Response:
        try:
            (
                http_status, message, data
            ) = UserController().get_detail(g.user_id)

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=data
            )
        except Exception as e:
            error_logger.error(f"Error on User Profile [GET] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class UserResetPasswordResource(Resource):
    def post(self) -> Response:
        try:
            input_data = request.get_json()
            schema = UserResetPasswordInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            http_status, message = UserController().reset_password(
                payload["username"], payload["password"]
            )
            return construct_api_response(http_status, message)

        except Exception as e:
            error_logger.error(f"Error on User Reset Password [POST] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class UserUnlockResource(Resource):
    def post(self) -> Response:
        try:
            input_data = request.get_json()
            schema = UserUnlockInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            http_status, message = UserController().unlock(
                payload["username"]
            )
            return construct_api_response(http_status, message)

        except Exception as e:
            error_logger.error(f"Error on User Reset Password [POST] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
