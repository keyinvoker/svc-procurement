from sqlalchemy.sql import func
from typing import List, Optional

from eproc.models.auth.roles_menus import RoleMenu
from eproc.models.auth.users_roles import UserRole


def get_user_roles(user_id: str) -> Optional[List[str]]:
    result = (
        UserRole.query
        .with_entities(func.array_agg(UserRole.role_id).label("role_id_list"))
        .filter(UserRole.user_id == user_id)
        .filter(UserRole.is_deleted.is_(False))
        .first()
    )

    role_id_list = None
    if result:
        role_id_list = result.role_id_list

    return role_id_list


def get_role_menus(role_id_list: List[str]) -> List[str]:
    result = (
        RoleMenu.query
        .with_entities(func.array_agg(RoleMenu.menu_id).label("menu_id_list"))
        .filter(RoleMenu.role_id.in_(role_id_list))
        .filter(RoleMenu.is_deleted.is_(False))
        .first()
    )

    menu_id_list = None
    if result:
        menu_id_list = result.menu_id_list
    
    return menu_id_list
