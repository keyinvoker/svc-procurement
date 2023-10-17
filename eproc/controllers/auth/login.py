import jwt
from hashlib import md5
from typing import Optional, Tuple

from eproc import error_logger
from eproc.models.users.users import User


class LoginController:
    def login(self, username: str, password: str) -> Tuple[bool, Optional[str]]:

        hashed_password = md5(
            password.encode("utf-8")
        ).hexdigest()

        user: User = (
            User.query
            .filter(User.username == username)  # TODO: use `uname` or just `usrid` || make sure `uname` cannot be edited first if want use `usrid`
            .first()
        )
        if not user:
            error_logger.error(f"Error on LoginController:login() :: Not found user: {username}")
            return False, None

        auth_token = None
        status = hashed_password.upper() == user.password

        if status:
            payload = dict(
                id=user.id,
                username=user.username,
            )
            auth_token = jwt.encode(payload, "secret", algorithm="HS256")

        return status, auth_token
