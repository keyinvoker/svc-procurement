from sqlalchemy import delete, insert
from traceback import format_exc
from typing import List, Optional, Tuple

from eproc import app_logger, error_logger
from eproc.models.auth.users_roles import UserRole
from eproc.models.base_model import session


def add_user_roles(
    user_id: str,
    role_id_list: List[str],
    existing_role_id_list: Optional[List[str]] = None,
) -> Tuple[List[str], List[str]]:

    successful_role_id_list = role_id_list.copy()
    failed_role_id_list = list()

    for role_id in role_id_list:
        log_data = f"user_id: {user_id}, role_id: {role_id}"

        if role_id in existing_role_id_list:
            successful_role_id_list.remove(role_id)
            failed_role_id_list.append(role_id)
            continue

        try:
            statement = insert(UserRole).values(
                user_id=user_id,
                role_id=role_id
            )
            session.execute(statement)
            session.commit()
            app_logger.info(f"Added to users_roles :: {log_data}")
        except Exception as e:
            session.rollback()
            error_logger.error(
                f"Error on add_user_roles() :: {log_data}, " +
                f"error: {e}, {format_exc()}"
            )

            successful_role_id_list.remove(role_id)
            failed_role_id_list.append(role_id)
    
    return successful_role_id_list, failed_role_id_list


def remove_user_roles(
    user_id: str,
    role_id_list: List[str],
    existing_role_id_list: Optional[List[str]] = None,
) -> Tuple[List[str], List[str]]:

    successful_role_id_list = existing_role_id_list.copy()
    failed_role_id_list = list()
    
    for existing_role_id in existing_role_id_list:
        log_data = f"user_id: {user_id}, role_id: {existing_role_id}"

        if existing_role_id in role_id_list:
            successful_role_id_list.remove(existing_role_id)
            failed_role_id_list.append(existing_role_id)
            continue

        try:
            statement = delete(UserRole).where(
                UserRole.user_id == user_id,
                UserRole.role_id == existing_role_id
            )
            session.execute(statement)
            session.commit()
            app_logger.info(f"Deleted from UserRole :: {log_data}")
        except Exception as e:
            session.rollback()
            error_logger.error(
                f"Error on remove_user_roles() :: {log_data}, " +
                f"error: {e}, {format_exc()}"
            )

            successful_role_id_list.remove(existing_role_id)
            failed_role_id_list.append(existing_role_id)
    
    return successful_role_id_list, failed_role_id_list


def update_user_roles(
    user_id: str,
    role_id_list: List[str],
    existing_role_id_list: Optional[List[str]] = None,
) -> Tuple[List[str], List[str]]:

    successful_add_role_id_list, failed_add_role_id_list = (
        add_user_roles(
            user_id=user_id,
            role_id_list=role_id_list,
            existing_role_id_list=existing_role_id_list,
        )
    )

    successful_remove_role_id_list, failed_remove_role_id_list = (
        remove_user_roles(
            user_id=user_id,
            role_id_list=role_id_list,
            existing_role_id_list=existing_role_id_list,
        )
    )

    return (
        successful_add_role_id_list,
        failed_add_role_id_list,
        successful_remove_role_id_list,
        failed_remove_role_id_list
    )
