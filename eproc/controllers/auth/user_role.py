from http import HTTPStatus
from sqlalchemy.sql import func
from typing import Optional, Tuple

from eproc.helpers.user_role import update_user_roles
from eproc.models.auth.roles import Role
from eproc.models.auth.users_roles import UserRole
from eproc.models.users.users import User
from eproc.schemas.auth.users_roles import UserRoleSchema


class UserRoleController:
    def __init__(self, **kwargs):
        self.model = UserRole
        self.schema = UserRoleSchema()
        self.many_schema = UserRoleSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, Optional[dict], int]:
        user_id: int = kwargs.get("user_id")

        query = (
            UserRole.query
            .with_entities(
                UserRole.user_id.label("user_id"),
                User.full_name.label("user_full_name"),
                func.array_agg(Role.id).label("role_id_list"),
                func.array_agg(Role.description).label("role_name_list"),
            )
            .join(User, User.id == UserRole.user_id)
            .join(Role, Role.id == UserRole.role_id)
            .filter(UserRole.is_deleted.is_(False))
            .group_by(
                User.id,
                UserRole.user_id,
            )
        )

        if user_id:
            query = query.filter(UserRole.user_id == user_id)

        total = query.count()
        results = query.all()
        if not results:
            return (
                HTTPStatus.NOT_FOUND,
                "User Roles tidak ditemukan.",
                dict(
                    user_id=user_id,
                    role_name_list=[],
                ),
                total
            )

        data = self.many_schema.dump(results)

        return (
            HTTPStatus.OK,
            "User Roles ditemukan.",
            data,
            total
        )
    
    def update_user_roles(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str]:

        user_id: str = kwargs.get("user_id")
        role_id_list: list = kwargs.get("role_id_list")

        user_role_data = (
            UserRole.query
            .with_entities(
                func.array_agg(UserRole.role_id).label("existing_role_id_list")
            )
            .filter(UserRole.user_id == user_id)
            .first()
        )
        if not user_role_data:
            return (
                HTTPStatus.NOT_FOUND,
                f"Tidak ditemukan data User Roles dengan user ID: {user_id}."
            )
        
        existing_role_id_list = user_role_data.existing_role_id_list

        (
            successful_add_role_id_list,
            failed_add_role_id_list,
            successful_remove_role_id_list,
            failed_remove_role_id_list
        ) = update_user_roles(
            user_id=user_id,
            role_id_list=role_id_list,
            existing_role_id_list=existing_role_id_list,
        )

        print(
            successful_add_role_id_list,
            failed_add_role_id_list,
            successful_remove_role_id_list,
            failed_remove_role_id_list
        )

        if (
            (failed_add_role_id_list) == (role_id_list)
            and (failed_remove_role_id_list) == (existing_role_id_list)
        ):
            return (
                HTTPStatus.CONFLICT,
                f"Tidak ada yang perlu diperbarui."
            )

        return (
            HTTPStatus.OK,
            f"Sukses memperbarui user dengan id: {user_id}. " +
            f"Role id yang berhasil ditambahkan: {successful_add_role_id_list}, " +
            f"yang gagal: {failed_add_role_id_list}. " +
            f"Role id yang berhasil dihapuskan: {successful_remove_role_id_list}, " +
            f"yang gagal: {failed_remove_role_id_list}."
        )
