from sqlalchemy.sql import func
from typing import List, Optional

from eproc.models.auth.users_roles import UserRole


def get_user_roles(user_id: str) -> Optional[List[str]]:
    result = (
        UserRole.query
        .with_entities(func.array_agg(UserRole.role_id).label("role_id_list"))
        .filter(UserRole.user_id == user_id)
        .filter(UserRole.is_deleted.is_(False))
        .group_by(UserRole.role_id)
        .order_by(UserRole.role_id)
        .first()
    )

    role_id_list = None
    if result:
        role_id_list = result.role_id_list

    return role_id_list
