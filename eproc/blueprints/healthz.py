import psycopg2
from flask import Blueprint, Response, current_app
from flask_restful import Api, Resource
from http import HTTPStatus
from traceback import format_exc

from eproc import error_logger
from eproc.tools.response import construct_api_response


def check_db() -> bool:
    DB_USER = current_app.config.get("DB_USER")
    DB_PASS = current_app.config.get("DB_PASS")
    DB_HOST = current_app.config.get("DB_HOST")
    DB_PORT = current_app.config.get("DB_PORT")
    DB_NAME = current_app.config.get("DB_NAME")

    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        error_logger.error(f"check_db() :: error: {e}, {format_exc()}")
        return False


class HealthzResource(Resource):
    def get(self) -> Response:
        """
        This API responses hello world in /_healthz path
        """

        is_db_healthy = None
        response = dict()
        response["status"] = dict(database=is_db_healthy)
        response["info"] = "Something went wrong!"

        try:
            is_db_healthy = check_db()

            if is_db_healthy:
                http_status = HTTPStatus.OK
                response["status"] = dict(database=is_db_healthy)
                response["info"] = "Server healthy! No error detected."

            return construct_api_response(
                http_status=http_status,
                data=response
            )

        except Exception as e:
            error_logger.error(f"Healthz [GET] :: error: {e}, {format_exc()}")
            return construct_api_response(
                http_status=http_status,
                data=response
            )


healthz_blueprint = Blueprint("healthz", __name__, url_prefix="/healthz")
healthz_api = Api(healthz_blueprint)
healthz_api.add_resource(HealthzResource, "")
