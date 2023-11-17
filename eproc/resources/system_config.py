from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.controllers.reference import ReferenceController
from eproc.schemas.references import SystemConfigGetInputSchema
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class SystemConfigResource(Resource):
    def get(self) -> Response:
        try:
            schema = SystemConfigGetInputSchema()

            is_valid, response, payload = schema_validate_and_load(
                schema=schema,
                payload=request.args.to_dict(),
            )
            if not is_valid:
                return response

            (
                http_status, message, data
            ) = ReferenceController().get_system_configuration(payload["option"])

            return construct_api_response(http_status, message, data)

        except Exception as e:
            error_logger.error(f"Error on Reference [GET]: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class ApprovalLimitPriceComparisonResource(Resource):
    def get(self) -> Response:
        try:
            return construct_api_response(HTTPStatus.OK)

        except Exception as e:
            error_logger.error(f"Error on ApprovalLimitPriceComparison [GET]: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class ApprovalLimitPurchaseOrderResource(Resource):
    def get(self) -> Response:
        try:
            return construct_api_response(HTTPStatus.OK)

        except Exception as e:
            error_logger.error(f"Error on ApprovalLimitPurchaseOrder [GET]: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class ApprovalLimitGoodsReceivedResource(Resource):
    def get(self) -> Response:
        try:
            return construct_api_response(HTTPStatus.OK)

        except Exception as e:
            error_logger.error(f"Error on ApprovalLimitGoodsReceived [GET]: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class PurchaseOrderResource(Resource):
    def get(self) -> Response:
        try:
            return construct_api_response(HTTPStatus.OK)

        except Exception as e:
            error_logger.error(f"Error on PurchaseOrder [GET]: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class SystemLockResource(Resource):
    def get(self) -> Response:
        try:
            return construct_api_response(HTTPStatus.OK)

        except Exception as e:
            error_logger.error(f"Error on SystemLock [GET]: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class PasswordResource(Resource):
    def get(self) -> Response:
        try:
            return construct_api_response(HTTPStatus.OK)

        except Exception as e:
            error_logger.error(f"Error on Password [GET]: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class AccessTimeResource(Resource):
    def get(self) -> Response:
        try:
            return construct_api_response(HTTPStatus.OK)

        except Exception as e:
            error_logger.error(f"Error on AccessTime [GET]: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class UploadResource(Resource):
    def get(self) -> Response:
        try:
            return construct_api_response(HTTPStatus.OK)

        except Exception as e:
            error_logger.error(f"Error on Upload [GET]: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )


class TaxResource(Resource):
    def get(self) -> Response:
        try:
            return construct_api_response(HTTPStatus.OK)

        except Exception as e:
            error_logger.error(f"Error on Tax [GET]: {e}, {format_exc()}")
            return construct_api_response(
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
