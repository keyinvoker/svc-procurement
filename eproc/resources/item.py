from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.item import ItemController
from eproc.helpers.commons import split_string_into_list
from eproc.schemas.items.items import (
    ItemGetInputSchema,
    ItemCategoryGetInputSchema,
)
from eproc.tools.response import make_json_response
from eproc.tools.validation import schema_validate_and_load


class ItemResource(Resource):
    def __init__(self):
        self.controller = ItemController()

    def get(self) -> Response:
        try:
            list_param_keys = [
                "id_list",
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
            error_logger.error(f"Error on Item [GET] :: {e}, {format_exc()}")
            return make_json_response(HTTPStatus.INTERNAL_SERVER_ERROR)


class ItemClassResource(Resource):
    def __init__(self):
        self.controller = ItemController()

    def get(self):
        try:
            (
                http_status, message, data
            ) = self.controller.get_classes()

            return make_json_response(
                http_status=http_status,
                message=message,
                data=data,
            )

        except Exception as e:
            error_logger.error(f"Error on Item Class [GET] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class ItemCategoryResource(Resource):
    def __init__(self):
        self.controller = ItemController()

    def get(self):
        try:
            schema = ItemCategoryGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=request.args.to_dict(),
            )
            if not is_valid:
                return response

            (
                http_status, message, data
            ) = self.controller.get_categories(**payload)

            return make_json_response(
                http_status=http_status,
                message=message,
                data=data,
            )

        except Exception as e:
            error_logger.error(f"Error on Item Category [GET] :: {e}, {format_exc()}")
            return make_json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
