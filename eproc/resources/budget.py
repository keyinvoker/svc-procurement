from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.budget import BudgetController
from eproc.helpers.commons import split_string_into_list
from eproc.schemas.budgets import BudgetGetInputSchema
from eproc.tools.response import make_json_response
from eproc.tools.validation import schema_validate_and_load


class BudgetResource(Resource):
    def __init__(self):
        self.controller = BudgetController()

    def get(self) -> Response:
        try:
            schema = BudgetGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=request.args.to_dict(),
            )
            if not is_valid:
                return response

            (
                http_status, message, data_list, total
            ) = self.controller.get_list(**payload)

            data = dict(
                data=data_list,
                total=total,
                limit=payload["limit"],
                offset=payload["offset"],
            )

            return make_json_response(
                http_status=http_status,
                message=message,
                data=data,
            )
        except Exception as e:
            error_logger.error(f"Error on Budget [GET] :: {e}, {format_exc()}")
            return make_json_response(HTTPStatus.INTERNAL_SERVER_ERROR)
