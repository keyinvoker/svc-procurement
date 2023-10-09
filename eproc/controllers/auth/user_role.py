from http import HTTPStatus
from sqlalchemy.sql import func
from typing import List, Optional, Tuple

from eproc import error_logger
from eproc.models.auth.roles import Role
from eproc.models.auth.users_roles import UserRole
from eproc.schemas.auth.users_roles import UserRoleSchema


class UserRoleController:
    def __init__(self, **kwargs):
        self.model = UserRole
        self.schema = UserRoleSchema
        self.many_schema = UserRoleSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:
        user_id: int = kwargs.get("user_id")

        query = (
            UserRole.query
            .with_entities(
                UserRole.user_id.label("user_id"),
                func.array_agg(Role.description).label("role_name_list"),
            )
            .join(Role, Role.id == UserRole.role_id)
            .filter(UserRole.user_id == user_id)
            .filter(UserRole.is_deleted.is_(False))
            .group_by(UserRole.user_id)
        )

        total = query.count()

        results: List[UserRole] = query.all()
        if not results:
            return (
                HTTPStatus.NOT_FOUND,
                "User Roles tidak ditemukan.",
                [],
                total
            )
        data_list = self.many_schema.dump(results)

        return (
            HTTPStatus.OK,
            "User Roles ditemukan.",
            data_list,
            total
        )
