import json
from flask import Response
from http import HTTPStatus
from typing import Optional, Union

from eproc.schemas.response import DefaultResponseSchema

default_messages: dict = {
    status: status.name.replace("_", " ").title()
    for status in HTTPStatus
}


def construct_api_response(
    http_status: Union[HTTPStatus, int],
    message: str = "",
    data: Optional[dict] = None,
) -> Response:

    if not message:
        message = default_messages[http_status]

    response_data = DefaultResponseSchema().dump(
        {"status": http_status.value, "message": message, "data": data}
    )

    return Response(
        response=json.dumps(response_data),
        status=http_status,
        mimetype="application/json",
    )
