from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.user import UserController
from eproc.helpers.commons import split_string_into_list
from eproc.schemas.users.users import UserGetInputSchema
from eproc.tools.response import make_json_response
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

            return make_json_response(
                http_status=http_status,
                message=message,
                data=data
            )
        except Exception as e:
            error_logger.error(f"Error on User [GET] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
    
    def post(self) -> Response:
        try:
            input_data = request.get_json()
            schema = ...

            is_valid, response, payload_list = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            UserController().insert(payload_list)

            return make_json_response(
                http_status=HTTPStatus.OK
            )
        except Exception as e:
            error_logger.error(f"Error on User [POST] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def put(self) -> Response:
        try:
            input_data = request.get_json()
            schema = ...

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response
            
            UserController().update(**payload)

            return make_json_response(
                http_status=HTTPStatus.OK
            )
        except Exception as e:
            error_logger.error(f"Error on User [PUT] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def delete(self) -> Response:
        try:
            input_data = request.get_json()
            schema = ...

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            return make_json_response(
                UserController().delete(payload["item_id_list"])
            )
        except Exception as e:
            error_logger.error(f"Error on User [DELETE] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class UserDetailResource(Resource):
    def get(self) -> Response:
        try:
            schema = ...

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=request.args.to_dict(),
            )
            if not is_valid:
                return response

            (
                http_status, message, data
            ) = UserController().get_detail(payload["id"])

            return make_json_response(
                http_status=http_status,
                message=message,
                data=data
            )
        except Exception as e:
            error_logger.error(f"Error on User Detail [GET] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
