from datetime import datetime
from flask import Response
from http import HTTPStatus
from sqlalchemy import insert
from typing import List, Optional, Tuple

from eproc import app_logger, error_logger
from eproc.models.base_model import session
from eproc.models.enums import Roles, TransactionType
from eproc.models.items.procurement_request_items import (
    ProcurementRequestItem
)
from eproc.tools.response import construct_api_response

# Procurement
ALL_PROCUREMENT_ADMIN_ROLES = [
    Roles.GA_AND_PROCUREMENT_ADMIN.value,
    Roles.GA_AND_PROCUREMENT_ADMIN_APPROVER_1.value,
    Roles.PR_REGULER_APPROVER_1.value,
    Roles.PR_REGULER_APPROVER_2.value,
]
ALL_PROCUREMENT_USER_ROLES = [
    Roles.PR_REGULER_LIST_ONLY.value,
    Roles.PR_REGULER_USER.value,
]
ALL_PROCUREMENT_ROLES = ALL_PROCUREMENT_ADMIN_ROLES + ALL_PROCUREMENT_USER_ROLES

# B2B
ALL_B2B_ADMIN_ROLES = [
    Roles.PR_B2B_APPROVER_1.value,
    Roles.PR_B2B_APPROVER_2.value,
]
ALL_B2B_USER_ROLES = [
    Roles.PR_B2B_LIST_ONLY.value,
    Roles.PR_B2B_USER.value,
]
ALL_B2B_ROLES = ALL_B2B_ADMIN_ROLES + ALL_B2B_USER_ROLES

# Project
ALL_PROJECT_ADMIN_ROLES = [
    Roles.PR_PROJECT_APPROVER_1.value,
    Roles.PR_PROJECT_APPROVER_2.value,
    Roles.PR_PROJECT_APPROVER_3.value,
    Roles.PR_PROJECT_APPROVER_4.value,
    Roles.PR_PROJECT_APPROVER_5.value,
    Roles.PR_PROJECT_APPROVER_6.value,
    Roles.PR_PROJECT_APPROVER_7.value,
]
ALL_PROJECT_USER_ROLES = [
    Roles.PR_PROJECT_USER.value,
    Roles.PR_PROJECT_LIST_ONLY.value,
]
ALL_PROJECT_ROLES = ALL_PROJECT_ADMIN_ROLES + ALL_PROJECT_USER_ROLES

ALL_ADMIN_ROLES = ALL_PROCUREMENT_ADMIN_ROLES + ALL_B2B_ADMIN_ROLES + ALL_PROJECT_ADMIN_ROLES
ALL_USER_ROLES = ALL_PROCUREMENT_USER_ROLES + ALL_B2B_USER_ROLES + ALL_PROJECT_USER_ROLES
ALL_ROLES = ALL_PROCUREMENT_ROLES + ALL_B2B_ROLES + ALL_PROJECT_ROLES


def has_corresponding_roles(
    user_roles: List[str],
    transaction_type: str,
) -> Tuple[bool, Optional[Response]]:

    if (
        (
            transaction_type == TransactionType.REG.name
            and not any(
                role in ALL_PROCUREMENT_ROLES
                for role in user_roles
            )
        )
        or (
            transaction_type == TransactionType.B2B.name
            and not any(
                role in ALL_B2B_ROLES
                for role in user_roles
            )
        )
        or (
            transaction_type == TransactionType.TDR.name
            and not any(
                role in ALL_PROJECT_ROLES
                for role in user_roles
            )
        )
    ):
        return False, construct_api_response(
            HTTPStatus.UNAUTHORIZED,
            "User tidak memiliki akses."
        )
    
    return True, None


def add_items(
    procurement_request_id: int,
    item_list: List[dict],
) -> Tuple[List[Optional[str]], List[Optional[dict]]]:

    failed_item_ids: List[Optional[str]] = list()
    failed_item_data: List[Optional[dict]] = list()

    for index, item in enumerate(item_list):
        try:
            item_id = item.get("id")
            unit_of_measurement = item.get("unit_of_measurement")
            quantity = item.get("quantity")
            required_date = item.get("required_date")
            required_days_interval = item.get("required_days_interval")
            notes = item.get("notes")

            statement = insert(ProcurementRequestItem).values(
                procurement_request_id=procurement_request_id,
                item_id=item_id,
                line_number=(index + 1),
                unit_of_measurement=unit_of_measurement,
                quantity=quantity,
                required_date=datetime.fromisoformat(required_date).replace(tzinfo=None),
                required_days_interval=required_days_interval,
                notes=notes,
                currency_id="IDR",
                aprqt=0,  # TODO: field gak guna
            )
            session.execute(statement)
            session.commit()

            app_logger.info(f"Added to procurement_request_items :: procurement_request_id: {procurement_request_id}, item_id: {item_id}")

        except Exception as e:
            session.rollback()
            error_logger.error(f"Failed to add PR Item :: {e}, data: {item}")

            failed_item_ids.append(item_id)
            failed_item_data.append(item)
            continue
    
    return failed_item_ids, failed_item_data
