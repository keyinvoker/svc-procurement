from flask import Response
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from procurement import error_logger
from procurement.controllers.auth.register import RegisterController
from procurement.tools.response import make_json_response


class RegisterResource(Resource):
    def get(self) -> Response:
        try:
            return make_json_response(
                http_status=HTTPStatus.OK
            )
        except Exception as e:
            error_logger.error(f"Error on Register [GET] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
    
    def post(self) -> Response:
        try:
            return make_json_response(
                http_status=HTTPStatus.OK
            )
        except Exception as e:
            error_logger.error(f"Error on Register [POST] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def put(self) -> Response:
        try:
            return make_json_response(
                http_status=HTTPStatus.OK
            )
        except Exception as e:
            error_logger.error(f"Error on Register [PUT] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def delete(self) -> Response:
        try:
            return make_json_response(
                http_status=HTTPStatus.OK
            )
        except Exception as e:
            error_logger.error(f"Error on Register [DELETE] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
