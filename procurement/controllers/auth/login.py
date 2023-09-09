from hashlib import sha256

from procurement.helpers.auth import get_salt_from_database
from procurement.models.users.admins import Admin


class LoginController:
    def __init__(self, **kwargs):
        self.email: str = kwargs.get("email")
        self.password: str = kwargs.get("password")

    def login(self) -> bool:
        salt = get_salt_from_database(self.email)

        salted_password = self.password + salt

        hashed_password = sha256(
            salted_password.encode("utf-8")
        ).hexdigest()

        admin: Admin = (
            Admin.query
            .filter(Admin.email == self.email)
            .first()
        )

        return hashed_password == admin.password
