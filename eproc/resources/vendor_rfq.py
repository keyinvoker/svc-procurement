from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.vendor_rfq import VendorRFQController
from eproc.helpers.commons import split_string_into_list
from eproc.schemas.vendor_rfqs import VendorRFQGetInputSchema
from eproc.tools.response import make_json_response
from eproc.tools.validation import schema_validate_and_load


class VendorRFQResource(Resource):
    def __init__(self):
        self.controller = VendorRFQController()

    def get(self) -> Response:
        if not request.headers.get("Authorization"):
            error_logger.error(f"Error auth :: no token")
            return make_json_response(HTTPStatus.UNAUTHORIZED, "Tidak ada token")
        elif request.headers.get("Authorization") != "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImFkbWluIiwidXNlcm5hbWUiOiJhZG1pbiJ9.SLxXsx0zGexZLlzjaZfy0LLtS39sSKIpU2O99UbP-50":
            return make_json_response(HTTPStatus.UNAUTHORIZED, "Token salah")

        try:
            list_param_keys = [
                "id_list",
            ]
            input_data = split_string_into_list(
                request.args.to_dict(),
                list_param_keys
            )
            schema = VendorRFQGetInputSchema()

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

            return make_json_response(
                http_status=http_status,
                message=message,
                data=data,
            )
        except Exception as e:
            error_logger.error(f"Error on Vendor RFQ [GET] :: {e}, {format_exc()}")
            return make_json_response(HTTPStatus.INTERNAL_SERVER_ERROR)
