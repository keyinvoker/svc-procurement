from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
from sqlalchemy import text
from traceback import format_exc

from eproc import db, error_logger
from eproc.helpers.commons import split_string_into_list
from eproc.tools.response import make_json_response
from eproc.tools.validation import schema_validate_and_load


class ProcurementRequestProgressResource(Resource):
    def get(self):
        try:
            raw_query = text("""
                select a.trnno, a.docno, a.descr,
                case when b.trnno is null then 'Process' else 'Final' end as temps
                from procurement_requests as a
                left join tivty as b on b.dref1 = a.docno
                order by a.trnno
            """)

            results = db.session.execute(raw_query).fetchall()
            total = len(results)

            in_process = 0
            final = 0
            for result in results:
                if result[3] == "Final":
                    final += 1
                elif result[3] == "Process":
                    in_process += 1
            
            in_process_percentage = round((in_process / total * 100), 2)
            final_percentage = round((final / total * 100), 2)

            data = dict(
                in_process_percentage=in_process_percentage,
                final_percentage=final_percentage,
            )
            return make_json_response(
                http_status=HTTPStatus.OK,
                data=data,
            )
        except Exception as e:
            error_logger.error(f"Error on PR Progress [GET] :: {e}, {format_exc()}")
            return make_json_response(HTTPStatus.INTERNAL_SERVER_ERROR)
