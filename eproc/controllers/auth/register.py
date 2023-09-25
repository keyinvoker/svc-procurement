import secrets
from hashlib import sha256
from http import HTTPStatus
from typing import Tuple

from eproc.models.users.users import User
from eproc.schemas.users.users import UserAutoSchema


class RegisterController:
    def __init__(self):
        self.admin_schema = UserAutoSchema()

    def register(
        self,
        name: str,
        employee_identification_number: str,
        email: str,
        password: str,
    ) -> Tuple[HTTPStatus, str, dict]:

        salt = secrets.token_hex(16)

        salted_password = password + salt
        hashed_password = sha256(
            salted_password.encode("utf-8")
        ).hexdigest()

        new_admin = User(
            name=name,
            employee_identification_number=employee_identification_number,
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
