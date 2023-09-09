from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from procurement import error_logger
from procurement.controllers.auth.login import LoginController
from procurement.schemas.auth.login import LoginInputSchema
from procurement.tools.response import make_json_response
from procurement.tools.validation import schema_validate_and_load


class LoginResource(Resource):
    def post(self) -> Response:
        try:
            input_data = request.get_json()
            schema = LoginInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            status = LoginController(**payload).login()
            if not status:
                return make_json_response(
                    http_status=HTTPStatus.UNAUTHORIZED,
                    message="Login gagal. Pastikan data yang dimasukkan benar."
                )

            return make_json_response(
                http_status=HTTPStatus.OK,
                message="Login berhasil."
            )
        except Exception as e:
            error_logger.error(f"Error on Login [POST] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
