from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from sqlalchemy import text
from traceback import format_exc

from eproc import db, error_logger
from eproc.helpers.commons import split_string_into_list
from eproc.tools.response import construct_api_response
from eproc.tools.validation import schema_validate_and_load


class ProcurementRequestProgressResource(Resource):
    def get(self) -> Response:
        try:
            raw_query = text("""
                SELECT status, COUNT(*) AS status_count
                FROM
                (
                    SELECT
                        CASE 
                            WHEN i.id IS NULL THEN 'In Process'
                            ELSE 'Final'
                        END AS status
                    FROM procurement_requests AS pr
                    LEFT JOIN inventories AS i ON i.dref1 = pr.document_number
                )
                GROUP BY status;
            """)

            results = db.session.execute(raw_query).fetchall()

            final = results[0].status_count
            in_process = results[1].status_count
            total = in_process + final
            
            in_process_percentage = round((in_process / total * 100), 2)
            final_percentage = round((final / total * 100), 2)

            data = dict(
                in_process_percentage=in_process_percentage,
                final_percentage=final_percentage,
            )
            return construct_api_response(
                http_status=HTTPStatus.OK,
                data=data,
            )
        except Exception as e:
            error_logger.error(f"Error on PR Progress [GET] :: {e}, {format_exc()}")
            return construct_api_response(HTTPStatus.INTERNAL_SERVER_ERROR)
