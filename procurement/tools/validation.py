from flask import Response
from http import HTTPStatus
from marshmallow import Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from typing import Optional, Tuple, Union

from procurement.tools.response import make_json_response


def schema_validate(
    schema: Union[Schema, SQLAlchemyAutoSchema],
    payload: dict,
    message: Optional[str] = "Terjadi ketidaksesuaian pada data yang dimasukkan."
) -> Tuple[bool, Optional[Response]]:

    validation_error = schema.validate(payload)
    if validation_error:
        if "_schema" in validation_error:
            validation_error["errors"] = validation_error["_schema"]
            del validation_error["_schema"]
        return False, make_json_response(
            http_status=HTTPStatus.BAD_REQUEST,
            message=message,
            data=validation_error
        )

    return True, None


def schema_validate_and_load(
    schema: Union[Schema, SQLAlchemyAutoSchema],
    payload: dict,
    message: Optional[str] = "Terjadi ketidaksesuaian pada data yang dimasukkan."
) -> Tuple[bool, Optional[Response], dict]:

    is_valid, response = schema_validate(
        schema=schema,
        payload=payload,
        message=message
    )

    if not is_valid:
        return False, response, {}
    
    return True, None, schema.load(payload)
