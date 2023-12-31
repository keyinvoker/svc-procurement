from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.purchase_order import PurchaseOrderController
from eproc.helpers.commons import split_string_into_list
from eproc.schemas.purchase_orders.purchase_orders import (
    PurchaseOrderGetInputSchema,
    PurchaseOrderDetailGetInputSchema,
    PurchaseOrderItemGetInputSchema,
    )
from eproc.tools.decorator import validate_token
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class PurchaseOrderResource(Resource):
    def __init__(self):
        self.controller = PurchaseOrderController()

    @validate_token
    def get(self) -> Response:
        try:
            list_param_keys = [
                "id_list",
            ]
            input_data = split_string_into_list(
                request.args.to_dict(),
                list_param_keys
            )
            schema = PurchaseOrderGetInputSchema()

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
            error_logger.error(f"Error on Vendor RFQ [GET] :: {e}, {format_exc()}")
            return construct_api_response(HTTPStatus.INTERNAL_SERVER_ERROR)


class PurchaseOrderDetailResource(Resource):
    @validate_token
    def get(self) -> Response:
        try:
            is_valid, response, payload = schema_validate_and_load(
                schema=PurchaseOrderDetailGetInputSchema(),
                payload=request.args.to_dict(),
            )
            if not is_valid:
                return response

            (
                http_status, message, data
            ) = PurchaseOrderController().get_detail(payload["id"])

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=data
            )
        except Exception as e:
            error_logger.error(f"Error on Procurement Request Detail [GET] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class PurchaseOrderItemResource(Resource):
    @validate_token
    def get(self) -> Response:
        try:
            is_valid, response, payload = schema_validate_and_load(
                schema=PurchaseOrderItemGetInputSchema(),
                payload=request.args.to_dict(),
            )
            if not is_valid:
                return response

            (
                http_status, message, data,
                total_amount,
                total_discount_amount,
                total_net_price,
                total_tax_amount,
                total_net_amount,
                total
            ) = PurchaseOrderController().get_items(
                **payload
            )

            data = dict(
                data=data,
                total_amount=total_amount,
                total_discount_amount=total_discount_amount,
                total_net_price=total_net_price,
                total_tax_amount=total_tax_amount,
                total_net_amount=total_net_amount,
                total=total,
                limit=payload["limit"],
                offset=payload["offset"],
            )

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=data
            )
        except Exception as e:
            error_logger.error(f"Error on Procurement Request Item [GET] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
