import secrets
from hashlib import sha256
from http import HTTPStatus
from typing import Tuple

from procurement.models.users.admins import Admin
from procurement.schemas.users.admins import AdminSchema


class RegisterController:
    def __init__(self, **kwargs) -> Tuple[HTTPStatus, str, dict]:
        self.admin_schema = AdminSchema()

    def register(self, **kwargs):
        email: str = kwargs.get("email")
        password: str = kwargs.get("password")
        employee_identification_number = kwargs.get("employee_identification_number")

        salt = secrets.token_hex(16)

        salted_password = password + salt
        hashed_password = sha256(
            salted_password.encode("utf-8")
        ).hexdigest()

        new_admin = Admin(
            email=email,
            password=hashed_password,
            salt=salt,
        ).save()
        new_admin_data = self.admin_schema.dump(new_admin)

        return (
            HTTPStatus.OK,
            "User admin baru berhasil didaftarkan.",
            new_admin_data
        )
