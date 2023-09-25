from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.vendor.vendor import VendorController
from eproc.helpers.commons import split_string_into_list
from eproc.schemas.vendors.vendors import (
    VendorDeleteInputSchema,
    VendorDetailGetInputSchema,
    VendorGetInputSchema,
    VendorPostInputSchema,
    VendorPutInputSchema,
)
from eproc.tools.response import make_json_response
from eproc.tools.validation import schema_validate_and_load


class VendorResource(Resource):
    def get(self) -> Response:
        try:
            list_param_keys = [
                "id_list",
            ]
            input_data = split_string_into_list(
                request.args.to_dict(),
                list_param_keys
            )
            schema = VendorGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            (
                http_status, message, data_list, total
            ) = VendorController().get_list(**payload)

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
            error_logger.error(f"Error on Vendor [GET] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
    
    def post(self) -> Response:
        try:
            input_data = request.get_json()
            schema = VendorPostInputSchema(many=True)

            is_valid, response, payload_list = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            VendorController().insert(payload_list)

            return make_json_response(
                http_status=HTTPStatus.OK
            )
        except Exception as e:
            error_logger.error(f"Error on Vendor [POST] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def put(self) -> Response:
        try:
            input_data = request.get_json()
            schema = VendorPutInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response
            
            VendorController().update(**payload)

            return make_json_response(
                http_status=HTTPStatus.OK
            )
        except Exception as e:
            error_logger.error(f"Error on Vendor [PUT] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def delete(self) -> Response:
        try:
            input_data = request.get_json()
            schema = VendorDeleteInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            return make_json_response(
                VendorController().delete(payload["item_id_list"])
            )
        except Exception as e:
            error_logger.error(f"Error on Vendor [DELETE] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class VendorDetailResource(Resource):
    def get(self) -> Response:
        try:
            schema = VendorDetailGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=request.args.to_dict(),
            )
            if not is_valid:
                return response

            (
                http_status, message, data
            ) = VendorController().get_detail(payload["id"])

            return make_json_response(
                http_status=http_status,
                message=message,
                data=data
            )
        except Exception as e:
            error_logger.error(f"Error on Vendor Detail [GET] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
