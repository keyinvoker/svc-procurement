import secrets
from hashlib import sha256
from http import HTTPStatus
from typing import Tuple

from procurement.models.users.admins import Admin
from procurement.schemas.users.admins import AdminSchema


class RegisterController:
    def __init__(self, **kwargs) -> Tuple[HTTPStatus, str, dict]:
        self.admin_schema = AdminSchema()

        self.name: str = kwargs.get("name")
        self.email: str = kwargs.get("email")
        self.password: str = kwargs.get("password")
        self.employee_identification_number: str = kwargs.get(
            "employee_identification_number"
        )

    def register(self):
        salt = secrets.token_hex(16)

        salted_password = self.password + salt
        hashed_password = sha256(
            salted_password.encode("utf-8")
        ).hexdigest()

        new_admin = Admin(
            name=self.name,
            email=self.email,
            password=hashed_password,
            salt=salt,
        ).save()
        new_admin_data = self.admin_schema.dump(new_admin)

        return (
            HTTPStatus.OK,
            "User admin baru berhasil didaftarkan.",
            new_admin_data
        )
