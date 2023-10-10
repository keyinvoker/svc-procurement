import secrets
import string
from hashlib import md5
from http import HTTPStatus
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from traceback import format_exc
from typing import List, Optional, Tuple

from eproc import app_logger, error_logger
from eproc.models.auth.users_roles import UserRole
from eproc.models.references import Reference
from eproc.models.users.employees import Employee
from eproc.models.users.users import User
from eproc.schemas.users.users import (
    UserAutoSchema,
    UserDetailSchema,
)


class UserController:
    def __init__(self):
        self.schema = UserAutoSchema()
        self.many_schema = UserAutoSchema(many=True)
        self.detail_schema = UserDetailSchema()
    
    def get_detail(self, id: str) -> Tuple[HTTPStatus, str, Optional[dict]]:
        FirstApprover = aliased(User)
        SecondApprover = aliased(User)
        ThirdApprover = aliased(User)

        user: User = (
            User.query
            .with_entities(
                User.id,
                User.full_name,
                User.password,
                User.password_length,
                User.email,
                FirstApprover.id.label("first_approver_id"),
                FirstApprover.full_name.label("first_approver_full_name"),
                FirstApprover.is_active.label("first_approver_is_active"),
                SecondApprover.id.label("second_approver_id"),
                SecondApprover.full_name.label("second_approver_full_name"),
                SecondApprover.is_active.label("second_approver_is_active"),
                ThirdApprover.id.label("third_approver_id"),
                ThirdApprover.full_name.label("third_approver_full_name"),
                ThirdApprover.is_active.label("third_approver_is_active"),
                User.is_active,
                User.is_locked,
                User.is_anonymous,
                User.is_admin,
                User.updated_at,
                User.updated_by,
            )
            .outerjoin(FirstApprover, FirstApprover.id == User.first_approver_id)
            .outerjoin(SecondApprover, SecondApprover.id == User.second_approver_id)
            .outerjoin(ThirdApprover, ThirdApprover.id == User.third_approver_id)
            .filter(User.id == id)
            .filter(User.is_deleted.is_(False))
            .first()
        )
        
        if not user:
            return (
                HTTPStatus.NOT_FOUND,
                "User tidak ditemukan.",
                None
            )

        user_data = self.detail_schema.dump(user)

        return HTTPStatus.OK, "User ditemukan.", user_data

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        FirstApprover = aliased(User)

        user_query = (
            User.query
            .with_entities(
                User.id,
                User.full_name,
                User.password,
                User.password_length,
                User.email,
                FirstApprover.full_name.label("first_approver_full_name"),
                User.is_active,
                User.is_locked,
                User.is_anonymous,
                User.is_admin,
                User.updated_at,
                User.updated_by,
                Reference.description.label("status"),
            )
            .outerjoin(FirstApprover, FirstApprover.id == User.first_approver_id)
            .join(Reference, Reference.id == User.reference_id)
            .filter(User.is_deleted.is_(False))
        )

        if id_list:
            user_query = user_query.filter(User.id.in_(id_list))
        
        if search_query:
            user_query = (
                user_query
                .filter(or_(
                    User.id.ilike(f"%{search_query}%"),
                    User.full_name.ilike(f"%{search_query}%"),
                ))
            )
        
        total = user_query.count()
        
        if limit:
            user_query = user_query.limit(limit)

        if offset > 0:
            user_query = user_query.offset(offset)
        
        user_list: List[User] = user_query.all()

        if not user_list:
            return (
                HTTPStatus.NOT_FOUND,
                "User tidak ditemukan.",
                [],
                total
            )
        user_data_list = self.many_schema.dump(user_list)

        return (
            HTTPStatus.OK,
            "User ditemukan.",
            user_data_list,
            total
        )

    def register_user(self, **kwargs) -> Tuple[HTTPStatus, str]:
        user_id = kwargs.get("id")
        email = kwargs.get("email")
        phone_number = kwargs.get("phone_number")

        user = (
            User.query
            .filter(User.id == user_id)
            .filter(User.is_deleted.is_(False))
            .first()
        )
        if user:
            return (
                HTTPStatus.CONFLICT,
                f"Sudah ada user dengan id: {user_id}"
            )

        # TODO? ini approver harus dari tabel `employee` ?
        first_approver_id = kwargs.get("first_approver_id")
        first_approver: Employee = (
            Employee.query
            .filter(Employee.id == first_approver_id)
            .filter(Employee.is_deleted.is_(False))
            .first()
        )
        if not first_approver:
            return (
                HTTPStatus.BAD_REQUEST,
                f"Tidak ditemukan pegawai yang ditunjuk sebagai approver dengan id: {first_approver_id}"
            )

        # Define the characters you want to include in the password
        characters = string.ascii_letters + string.digits + "!#$%&@"
        password_length = 12
        raw_password = "".join(secrets.choice(characters) for _ in range(password_length))
        hashed_password = (
            md5(raw_password.encode("utf-8"))
            .hexdigest()
            .upper()
        )

        try:
            data = dict()
            data["id"] = user_id
            data["username"] = user_id
            data["email"] = email
            data["phone_number"] = phone_number
            data["password"] = hashed_password
            data["password_length"] = password_length
            data["first_approver_id"] = first_approver_id
            data["is_head_office_user"] = True
            user = User(**data).save()
        except Exception as e:
            error_logger.error(f"Error on UserController:register_user() while saving user :: user_id: {user_id}, error: {e}, {format_exc()}")
            return (
                HTTPStatus.INTERNAL_SERVER_ERROR,
                f"Terjadi kesalahan saat menyimpan user dengan id: {user_id}"
            )

        # TODO: email the user with the password and proposed roles and approver with the approval request
        app_logger.info(f"UserController:register_user() :: creation email to be sent to: {email}")
        app_logger.info(f"UserController:register_user() :: approval request email to be sent to: {first_approver.email}")

        successful_role_id_list: list = kwargs.get("role_id_list").copy()
        failed_role_id_list = list()
        for role_id in kwargs.get("role_id_list"):
            try:
                UserRole(user_id=user_id, role_id=role_id).save()
            except Exception as e:
                successful_role_id_list.remove(role_id)
                failed_role_id_list.append(role_id)
                error_logger.error(f"Error on UserController:register_user() while saving roles :: user_id: {user_id}, role_id: {role_id}, error: {e}, {format_exc()}")

        return (
            HTTPStatus.CREATED,
            f"Sukses menyimpan user dengan id: {user_id}. " +
            f"Role id yang berhasil ditambahkan: {successful_role_id_list}, " +
            f"yang gagal: {failed_role_id_list}."
        )
