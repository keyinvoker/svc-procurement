import jwt
from datetime import timedelta
from hashlib import md5
from typing import Optional, Tuple
from traceback import format_exc

from eproc import error_logger
from eproc.helpers.commons import wibnow
from eproc.models.auth.user_tokens import UserToken
from eproc.models.users.users import User


class LoginController:
    def login(self, username: str, password: str) -> Tuple[bool, Optional[str]]:
        try:
            hashed_password = md5(
                password.encode("utf-8")
            ).hexdigest()

            user: User = (
                User.query
                .filter(User.username == username)
                .first()
            )
            if not user:
                error_logger.error(f"Error on LoginController:login() :: Not found user: {username}")
                return False, None

            auth_token = None
            status = hashed_password.upper() == user.password

            if status:
                expires_at = wibnow() + timedelta(hours=1)

                auth_token = jwt.encode(
                    payload={
                        "username": user.username,
                        "expires_at": str(expires_at)
                    },
                    key="secret",
                    algorithm="HS256"
                )

                UserToken(
                    user_id=user.id,
                    auth_token=auth_token,
                    expires_at=expires_at
                ).save()

            return status, auth_token

        except Exception as e:
            error_logger.error(f"Error on LoginController:login() :: {e}, {format_exc()}")
            return False, None
