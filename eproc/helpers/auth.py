from sqlalchemy import text
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from typing import List, Optional
from traceback import format_exc

from eproc import db, error_logger
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

    try:
        features = (
            db.session
            .query(
                Menu.id.label('menu_id'),
                Menu.menu_tag.label('menu_tag'),
                func.array_agg(Feature.id).label('feature_id_list'),
                func.array_agg(Feature.menu_tag).label('feature_tag_list')
            )
            .join(Feature, Feature.parent_id == Menu.id)
            .order_by(Menu.menu_tag, Feature.menu_tag)
            .group_by(Menu.id,Menu.menu_tag,Feature.menu_tag)
            .subquery('features')
        )

        role_info = (
            db.session
            .query(
                UserRole.user_id,
                Role.id.label("role_id"),
                Role.description.label("role_description"),
                Module.id.label("module_id"),
                Module.menu_tag.label("module_tag"),
                Module.is_parent.label("module_is_parent"),
                Menu.id.label("menu_id"),
                Menu.menu_tag.label("menu_tag"),
                Menu.is_parent.label("menu_is_parent"),
                features.c.feature_id_list,
                features.c.feature_tag_list
            )
            .join(Role, Role.id == UserRole.role_id)
            .join(RoleMenu, RoleMenu.role_id == Role.id)
            .join(Module, Module.id == RoleMenu.menu_id)
            .join(Menu, Menu.parent_id == Module.id)
            .outerjoin(features, features.c.menu_id == Menu.id)
            .filter(UserRole.user_id == user_id)
            .group_by(
                UserRole.user_id,
                Role.id,
                Module.id,
                Module.menu_tag,
                Menu.id,
                Menu.menu_tag,
                features.c.feature_tag_list,
                features.c.feature_id_list
            )
            .order_by(Module.menu_tag)
            .all()
        )

        results = list()  # TODO: Show for different roles.
        result = {
            "role_id": "",
            "role_description": "",
            "module_list": list(),
        }

        current_role = None
        current_module = None
        current_menu = None

        for info in role_info:
            (
                user_id,
                role_id,
                role_description,
                module_id,
                module_description,
                module_is_parent,
                menu_id,
                menu_description,
                menu_is_parent,
                feature_id_list,
                feature_description_list
            ) = info

            if current_role is None or current_role != role_id:
                current_role = role_id
                result["role_id"] = role_id
                result["role_description"] = role_description

            if current_module is None or current_module["module_id"] != module_id:
                print(f"triggered :: current: {current_module if not current_module else current_module.get('module_id')} --- {module_id} :id")
                current_module = {
                    "module_id": module_id,
                    "module_description": module_description,
                    "module_is_parent": module_is_parent,
                    "menu_list": list(),
                }
                result["module_list"].append(current_module)

            if module_is_parent:
                if current_menu is None or current_menu["menu_id"] != menu_id:
                    current_menu = {
                        "menu_id": menu_id,
                        "menu_description": menu_description,
                        "menu_is_parent": menu_is_parent,
                        "feature_list": list(),
                    }
                    current_module["menu_list"].append(current_menu)

                if menu_is_parent:
                    features = list()
                    for i in range(len(feature_id_list)):
                        feature = {
                            "feature_id": feature_id_list[i],
                            "feature_description": feature_description_list[i],
                        }
                        features.append(feature)

                    current_menu["feature_list"] = features

        return result

    except Exception as e:
        db.session.rollback()
        error_logger.error(f"Error on helpers.auth:get_user_info :: {e}, {format_exc()}")
        return {}
