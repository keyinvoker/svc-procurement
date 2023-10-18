import secrets
import string
from hashlib import md5
from http import HTTPStatus
from sqlalchemy import insert, or_
from sqlalchemy.orm import aliased
from traceback import format_exc
from typing import List, Optional, Tuple

from eproc import app_logger, error_logger
from eproc.models.auth.users_roles import UserRole
from eproc.models.base_model import session
from eproc.models.companies.branches import Branch
from eproc.models.companies.departments import Department
from eproc.models.companies.directorates import Directorate
from eproc.models.companies.divisions import Division
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
                Employee.branch_id,
                Branch.description.label("branch_name"),
                Employee.directorate_id,
                Directorate.description.label("directorate_name"),
                Employee.division_id,
                Division.description.label("division_name"),
                Employee.department_id,
                Department.description.label("department_name"),
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
            .outerjoin(Employee, Employee.id == User.id)
            .outerjoin(FirstApprover, FirstApprover.id == User.first_approver_id)
            .outerjoin(SecondApprover, SecondApprover.id == User.second_approver_id)
            .outerjoin(ThirdApprover, ThirdApprover.id == User.third_approver_id)
            .outerjoin(Branch, Branch.id == Employee.branch_id)
            .outerjoin(Directorate, Directorate.id == Employee.directorate_id)
            .outerjoin(Division, Division.id == Employee.division_id)
            .outerjoin(Department, Department.id == Employee.department_id)
            .filter(User.id == id)
            .filter(User.is_deleted.is_(False))
            .first()
        )
        
        if not user:
            return (
                HTTPStatus.NOT_FOUND,
                "Detail user tidak ditemukan.",
                None
            )

        user_data = self.detail_schema.dump(user)

        return HTTPStatus.OK, "Detail user ditemukan.", user_data

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        status_id: int = kwargs.get("status_id")
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
            .order_by(User.id)
        )

        if id_list:
            user_query = user_query.filter(User.id.in_(id_list))
        
        if status_id:
            user_query = user_query.filter(User.reference_id == status_id)
        
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
                # UserRole(user_id=user_id, role_id=role_id).save()
                statement = insert(UserRole).values(user_id=user_id, role_id=role_id)
                session.execute(statement)
            except Exception as e:
                session.rollback()
                successful_role_id_list.remove(role_id)
                failed_role_id_list.append(role_id)
                error_logger.error(f"Error on UserController:register_user() while saving roles :: user_id: {user_id}, role_id: {role_id}, error: {e}, {format_exc()}")

        return (
            HTTPStatus.CREATED,
            f"Sukses menyimpan user dengan id: {user_id}. " +
            f"Role id yang berhasil ditambahkan: {successful_role_id_list}, " +
            f"yang gagal: {failed_role_id_list}."
        )

    def reset_password(self, username: str, password: str) -> Tuple[HTTPStatus, str]:
        user: User = (
            User.query
            .filter(User.username == username)
            .filter(User.is_deleted.is_(False))
            .first()
        )
        if not user:
            return (
                HTTPStatus.NOT_FOUND,
                f"Tidak ditemukan username: {username}"
            )

        hashed_password = (
            md5(password.encode("utf-8"))
            .hexdigest()
            .upper()
        )

        user.password = hashed_password
        user.save()

        # TODO: send email to user with raw password

        return (
            HTTPStatus.OK,
            "Password berhasil diatur ulang."
        )
    
    def unlock(self, username: str):
        user: User = (
            User.query
            .filter(User.username == username)
            .filter(User.is_deleted.is_(False))
            .first()
        )
        if not user:
            return (
                HTTPStatus.NOT_FOUND,
                f"Tidak ditemukan username: {username}"
            )

        if user.is_locked == False:
            return (
                HTTPStatus.BAD_REQUEST,
                "User tidak terkunci."
            )

        user.is_locked = False
        user.save()

        return (
            HTTPStatus.OK,
            "User berhasil di-unlock."
        )
