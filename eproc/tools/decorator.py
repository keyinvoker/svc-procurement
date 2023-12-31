from flask import Response, g, request
from functools import wraps
from http import HTTPStatus
from typing import Callable, List, Optional, Union

from eproc.helpers.auth import (
    get_role_menus,
    get_user_roles,
)
from eproc.helpers.commons import wibnow
from eproc.models.auth.user_tokens import UserToken
from eproc.models.enums import Roles
from eproc.tools.response import construct_api_response


def validate_token(
    func: Optional[Callable] = None,
    *,
    admin_only: bool = False,
    allowlist: List[Optional[str]] = [],
) -> Callable:

    def decorate(_function):
        @wraps(_function)
        def wrapper(*args, **kwargs) -> Union[Callable, Response]:

            if not request.headers.get("Authorization"):
                return construct_api_response(
                    HTTPStatus.UNAUTHORIZED,
                    "Token kosong."
                )

            split_token = request.headers.get("Authorization").split(" ")
            if split_token[0] != "Bearer":
                return construct_api_response(
                    HTTPStatus.UNAUTHORIZED,
                    "Token salah."
                )

            user_token: UserToken = (
                UserToken.query
                .filter(
                    UserToken.auth_token == split_token[1],
                    UserToken.is_deleted.is_(False),
                )
                .first()
            )
            if not user_token:
                return construct_api_response(
                    HTTPStatus.UNAUTHORIZED,
                    "Token salah."
                )

            if user_token.is_active is False:
                return construct_api_response(
                    HTTPStatus.UNAUTHORIZED,
                    "Token sudah kedaluwarsa."
                )
            elif wibnow() > user_token.expires_at:
                user_token.is_active = False
                user_token.update()

                return construct_api_response(
                    HTTPStatus.UNAUTHORIZED,
                    "Token sudah kedaluwarsa."
                )

            roles = get_user_roles(user_token.user_id)
            if not roles:
                return construct_api_response(
                    HTTPStatus.UNAUTHORIZED,
                    "User tidak memiliki role."
                )

            g.user_id = user_token.user_id
            g.auth_token = user_token.auth_token
            g.roles = roles
            g.menus = get_role_menus(g.roles)

            if (
                admin_only
                and not Roles.ADMIN.value in roles
            ):
                return construct_api_response(
                    HTTPStatus.UNAUTHORIZED,
                    "User bukan admin."
                )

            if len(allowlist) > 0:
                if (
                    not Roles.ADMIN.value in allowlist
                    and not any(
                        role in allowlist
                        for role in roles
                    )
                ):
                    return construct_api_response(
                        HTTPStatus.UNAUTHORIZED,
                        "User tidak memiliki akses."
                    )

            return _function(*args, **kwargs)

        return wrapper
    
    if not func:
        return decorate
    else:
        return decorate(func)
