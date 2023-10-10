from http import HTTPStatus
from sqlalchemy.sql import func
from typing import List, Optional, Tuple

from eproc import error_logger
from eproc.models.auth.roles import Role
from eproc.models.auth.users_roles import UserRole
from eproc.schemas.auth.users_roles import UserRolesSchema


class UserRoleController:
    def __init__(self, **kwargs):
        self.model = UserRole
        self.schema = UserRolesSchema()

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, Optional[dict]]:
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

        result = query.first()
        if not result:
            return (
                HTTPStatus.NOT_FOUND,
                "User Roles tidak ditemukan.",
                dict(
                    user_id=user_id,
                    role_name_list=[],
                    is_registered=False,
                    total=0
                )
            )

        total = len(result.role_name_list)
        data = self.schema.dump(result)
        data["is_registered"] = True
        data["total"] = total

        return (
            HTTPStatus.OK,
            "User Roles ditemukan.",
            data
        )
