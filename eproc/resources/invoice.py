from flask import Response, g, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.invoice import InvoiceController
from eproc.helpers.commons import split_string_into_list
from eproc.models.invoices import Invoice
from eproc.schemas.invoices import (
    InvoiceGetInputSchema,
    InvoicePostInputSchema,
)
from eproc.tools.decorator import validate_token
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class InvoiceResource(Resource):
    def __init__(self):
        self.controller = InvoiceController()

    def get(self) -> Response:
        try:
            list_param_keys = [
                "id_list",
            ]
            input_data = split_string_into_list(
                request.args.to_dict(),
                list_param_keys
            )
            schema = InvoiceGetInputSchema()

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
            error_logger.error(f"Error on Invoice [GET] :: {e}, {format_exc()}")
            return construct_api_response(HTTPStatus.INTERNAL_SERVER_ERROR)
    
    @validate_token
    def post(self):
        try:
            # print()
            # print(request.files.to_dict())
            # print()
            invoice_image = (
                request.files.to_dict()
                .get("invoice_image")
            )
            if not invoice_image:
                return construct_api_response(
                    HTTPStatus.BAD_REQUEST,
                    "Mohon masukkan file."
                )

            input_data = request.form.to_dict()

            schema = InvoicePostInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=input_data,
            )
            if not is_valid:
                return response

            payload["image_path"] = f"/path/to/{invoice_image}"
            payload["updated_by"] = g.user_id

            http_status, message, data = self.controller.create(**payload)

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=data,
            )
        except Exception as e:
            error_logger.error(f"Error on Invoice [POST] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class InvoiceDetailResource(Resource):
    def __init__(self):
        self.controller = InvoiceController()

    def get(self) -> Response:
        try:
            return construct_api_response(
                self.controller(id)
            )
        except Exception as e:
            error_logger.error(f"Error on Invoice Detail [GET] :: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

class InvoiceTerminResource(Resource):
    def get(self) -> Response:
        payload = request.args.to_dict()

        print(payload)

        if not payload.get("purchase_order_id"):
            return construct_api_response(HTTPStatus.BAD_REQUEST, "Please input PO number.")

        invoice: Invoice = (
            Invoice.query
            .filter(
                Invoice.purchase_order_id == int(payload.get("purchase_order_id")),
                Invoice.is_deleted.is_(False)
            )
            .order_by(Invoice.termin.desc())
            .first()
        )

        if not invoice:
            next_termin = 1
        else:
            next_termin = invoice.termin + 1

        data = dict(next_termin=next_termin)

        return construct_api_response(HTTPStatus.OK, "", data)
