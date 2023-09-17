from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from procurement import error_logger
from procurement.controllers.auth.register import RegisterController
from procurement.schemas.auth.register import RegisterInputSchema
from procurement.tools.response import make_json_response
from procurement.tools.validation import schema_validate_and_load


class RegisterResource(Resource):
    def post(self) -> Response:
        try:
            input_data = request.get_json()
            schema = RegisterInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            return make_json_response(
                RegisterController().register(
                    name=payload["name"],
                    employee_identification_number=payload["employee_identification_number"],
                    email=payload["email"],
                    password=payload["password"],
                )
            )
        except Exception as e:
            error_logger.error(f"Error on Register [POST] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
