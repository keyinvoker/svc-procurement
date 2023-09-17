from hashlib import sha256

from procurement.helpers.auth import get_salt_from_database
from procurement.models.users.admins import Admin


class LoginController:
    def login(self, email: str, password: str) -> bool:
        salt = get_salt_from_database(email)

        salted_password = password + salt

        hashed_password = sha256(
            salted_password.encode("utf-8")
        ).hexdigest()

        admin: Admin = (
            Admin.query
            .filter(Admin.email == email)
            .first()
        )

        return hashed_password == admin.password
