from sqlalchemy import text
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from typing import List, Optional

from eproc.models.auth.menus import Menu
from eproc.models.auth.roles import Role
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


# TODO: URGENT: incomplete
def get_user_role_info(user_id: str) -> Optional[dict]:
    """
    The current `menus` table consists of 3 levels (`level`):
    - Level 1: Module
    - Level 2: Menu
    - Level 3: Feature

    A feature must have a parent menu.
    A menu must have a parent module.
    A module is at the top level.

    This function returns what each of user's roles accesses, per level.
    """

    Module = aliased(Menu)
    Feature = aliased(Menu)

    module_tag_list = func.array_agg(Module.menu_tag).label("module_tag_list")
    menu_tag_list = func.array_agg(Menu.menu_tag).label("menu_tag_list")
    feature_tag_list = func.array_agg(Feature.menu_tag).label("feature_tag_list")

    raw_query = text(
        """
        SELECT
            users.id "id",
            roles.id "role_id", roles.description "role_description",
            modules.id "module_id", modules.menu_tag "module_tag",
            array_agg(menus.id) "menu_id_list", array_agg(menus.menu_tag) "menu_tag_list",
            features.feature_id_list, features.feature_tag_list
        FROM users
        JOIN users_roles ON users_roles.user_id = users.id
        JOIN roles ON roles.id = users_roles.role_id
        JOIN roles_menus ON roles_menus.role_id = roles.id
        JOIN menus AS modules ON modules.id = roles_menus.menu_id
        JOIN menus ON menus.parent_id = modules.id
        LEFT JOIN (
            SELECT
                menus.id "menu_id", menus.menu_tag "menu_tag",
                array_agg(features.id) "feature_id_list", array_agg(features.menu_tag) "feature_tag_list"
            FROM menus
            JOIN menus AS features ON features.parent_id = menus.id
            GROUP BY menus.id
            ORDER BY menus.id
        ) AS features ON features.menu_id = menus.id
        WHERE users.id = 'jojo'
        GROUP BY users.id, roles.id, modules.id, features.feature_tag_list, features.feature_id_list
        ORDER BY modules.id;
        """
    )


    role_list = get_user_roles(user_id)
    if not role_list:
        return
