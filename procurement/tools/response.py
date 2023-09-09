import json
from flask import Response
from http import HTTPStatus
from typing import Optional, Union

from procurement.schemas.response import (
    DefaultResponseSchema,
    DefaultStringResponseSchema,
)

default_messages: dict = {
    status: status.name.replace("_", " ").title()
    for status in HTTPStatus
}


def make_json_response(
    http_status: Union[HTTPStatus, int],
    message: str = "",
    data: Optional[dict] = None,
) -> Response:

    if not message:
        message = default_messages[http_status]

    if data:
        if data == {}:
            if len(data) > 0:
                response_data = DefaultResponseSchema().dump(
                    {"message": message, "code": http_status.value}
                )
                response_data["data"] = data
        else:
            response_data = DefaultStringResponseSchema().dump(
                {"message": message, "code": http_status.value, "data": data}
            )
    elif data == []:
        response_data = DefaultStringResponseSchema().dump(
            {"message": message, "code": http_status.value, "data": data}
        )
    else:
        response_data = DefaultResponseSchema().dump(
            {"message": message, "code": http_status.value, "data": data}
        )

    return Response(
        response=json.dumps(response_data),
        status=http_status,
        mimetype="application/json",
    )
