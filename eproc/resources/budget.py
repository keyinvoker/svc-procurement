import pandas as pd
from flask import Response, g, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.budget import BudgetController
from eproc.schemas.budgets import BudgetGetInputSchema
from eproc.tools.decorator import validate_token
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class BudgetResource(Resource):
    def __init__(self):
        self.controller = BudgetController()

    @validate_token
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

            return construct_api_response(
                http_status=http_status,
                message=message,
                data=data,
            )
        except Exception as e:
            error_logger.error(f"Error on Budget [GET] :: {e}, {format_exc()}")
            return construct_api_response(HTTPStatus.INTERNAL_SERVER_ERROR)


class BudgetFileUploadResource(Resource):
    def __init__(self):
        self.controller = BudgetController()

    @validate_token
    def post(self):
        try:
            print(request.files.to_dict())
            file = request.files.to_dict().get("file")
            if not file:
                return construct_api_response(
                    HTTPStatus.BAD_REQUEST,
                    "Mohon masukkan file."
                )

            df = pd.read_csv(file, header=0)

            http_status, message = self.controller.file_upload(
                user_id=g.user_id,
                df=df,
            )

            return construct_api_response(
                http_status=http_status,
                message=message,
            )
        except Exception as e:
            error_logger.error(f"Error on Budget File Upload [POST] :: {e}, {format_exc()}")
            return construct_api_response(HTTPStatus.INTERNAL_SERVER_ERROR)
