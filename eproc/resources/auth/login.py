from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.auth.login import LoginController
from eproc.schemas.auth.login import LoginInputSchema
from eproc.tools.response import make_json_response
from eproc.tools.validation import schema_validate_and_load


class LoginResource(Resource):
    def post(self) -> Response:
        try:
            input_data = request.get_json()
            from eproc import app_logger
            app_logger.info(f"input_data :: {input_data}")
            schema = LoginInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            app_logger.info(f"payload :: {payload}")

            status = LoginController().login(
                username=payload["username"],
                password=payload["password"],
            )
            if not status:
                return make_json_response(
                    http_status=HTTPStatus.UNAUTHORIZED,
                    message="Login gagal. Pastikan data yang dimasukkan benar."
                )
            
            data = dict(
                token=""
            )

            return make_json_response(
                http_status=HTTPStatus.OK,
                message="Login berhasil.",
                data=data
            )
        except Exception as e:
            error_logger.error(f"Error on Login [POST] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
