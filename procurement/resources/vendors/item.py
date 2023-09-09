from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from procurement import error_logger
from procurement.controllers.vendor.item import ItemController
from procurement.helpers.commons import split_string_into_list
from procurement.schemas.vendors.items import (
    ItemDeleteInputSchema,
    ItemGetInputSchema,
    ItemPostInputSchema,
    ItemPutInputSchema,
)
from procurement.tools.response import make_json_response
from procurement.tools.validation import schema_validate_and_load


class ItemResource(Resource):
    def get(self) -> Response:
        try:
            list_param_keys = [
                "item_id_list",
                "category_list",
            ]
            input_data = split_string_into_list(
                request.args.to_dict(),
                list_param_keys
            )
            schema = ItemGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            (
                http_status, message, item_data_list, total
            ) = ItemController(**payload).get_list()

            data = dict(
                data=item_data_list,
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
            error_logger.error(f"Error on Item [GET] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
    
    def post(self) -> Response:
        try:
            input_data = request.get_json()
            schema = ItemPostInputSchema(many=True)

            is_valid, response, payload_list = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            ItemController().insert(payload_list)

            return make_json_response(
                http_status=HTTPStatus.OK
            )
        except Exception as e:
            error_logger.error(f"Error on Item [POST] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def put(self) -> Response:
        try:
            input_data = request.get_json()
            schema = ItemPutInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response
            
            ItemController(**payload).update()

            return make_json_response(
                http_status=HTTPStatus.OK
            )
        except Exception as e:
            error_logger.error(f"Error on Item [PUT] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def delete(self) -> Response:
        try:
            input_data = request.get_json()
            schema = ItemDeleteInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            return make_json_response(
                ItemController(**payload).delete()
            )
        except Exception as e:
            error_logger.error(f"Error on Item [DELETE] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
