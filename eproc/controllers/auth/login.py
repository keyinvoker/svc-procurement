from hashlib import md5

from eproc import error_logger
from eproc.models.users.users import User


class LoginController:
    def login(self, username: str, password: str) -> bool:

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
            return False

        return hashed_password.upper() == user.password
