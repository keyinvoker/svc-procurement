from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.price_comparison import PriceComparisonController
from eproc.helpers.commons import split_string_into_list
from eproc.schemas.price_comparisons import PriceComparisonGetInputSchema
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class PriceComparisonResource(Resource):
    def __init__(self):
        self.controller = PriceComparisonController()

    def get(self) -> Response:
        try:
            list_param_keys = [
                "id_list",
            ]
            input_data = split_string_into_list(
                request.args.to_dict(),
                list_param_keys
            )
            schema = PriceComparisonGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
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

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=data,
            )
        except Exception as e:
            error_logger.error(f"Error on Price Comparison [GET] :: {e}, {format_exc()}")
            return construct_api_response(HTTPStatus.INTERNAL_SERVER_ERROR)
