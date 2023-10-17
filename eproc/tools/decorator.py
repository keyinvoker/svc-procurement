from flask import Response, g, request
from functools import wraps
from http import HTTPStatus
from typing import Callable, Optional, Union

from eproc.helpers.auth import get_user_roles
from eproc.helpers.commons import wibnow
from eproc.models.auth.user_tokens import UserToken
from eproc.tools.response import make_json_response


def validate_token(
    func: Optional[Callable] = None,
) -> Callable:

    @wraps(func)
    def wrapper(*args, **kwargs) -> Union[Callable, Response]:

        if not request.headers.get("Authorization"):
            return make_json_response(
                HTTPStatus.UNAUTHORIZED,
                "Token kosong."
            )

        split_token = request.headers.get("Authorization").split(" ")
        if split_token[0] != "Bearer":
            return make_json_response(
                HTTPStatus.UNAUTHORIZED,
                "Token salah."
            )

        user_token: UserToken = (
            UserToken.query
            .filter(
                UserToken.auth_token == split_token[1],
                UserToken.is_active.is_(True),
                UserToken.is_deleted.is_(False),
            )
            .first()
        )
        if not user_token:
            return make_json_response(
                HTTPStatus.UNAUTHORIZED,
                "Token salah."
            )

        if wibnow() > user_token.expires_at:
            user_token.is_active = False
            user_token.update()

            return make_json_response(
                HTTPStatus.UNAUTHORIZED,
                "Token sudah kedaluwarsa."
            )

        g.roles = get_user_roles(user_token.user_id)

        return func(*args, **kwargs)

    return wrapper
