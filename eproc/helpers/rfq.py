from sqlalchemy import insert
from sqlalchemy.sql import func
from traceback import format_exc
from typing import List, Optional, Tuple

from eproc import app_logger, error_logger
from eproc.models.base_model import session
from eproc.models.items.procurement_request_items import ProcurementRequestItem
from eproc.models.rfqs.rfq_items import RFQItem


def get_next_document_number(
    year: int,
    month: int,
    sequence_number: int,
) -> str:

    try:
        year_string = str(year)[::2]
        month_string = str(month).zfill(2)
        sequence_string = str(sequence_number).zfill(4)

        document_number = f"BSS/RFQ/{year_string}{month_string}{sequence_string}"

        return document_number

    except Exception as e:
        error_logger.error(f"Error on helpers:rfq:get_next_document_number() :: {e}, {format_exc()}")


def add_items(
    rfq_id: int,
    purchase_request_id_list: List[int]
) -> List[Optional[str]]:
    
    failed_item_ids: List[Optional[str]] = list()

    items: List[ProcurementRequestItem] = (
        ProcurementRequestItem.query
        .filter(
            ProcurementRequestItem.procurement_request_id
            .in_(purchase_request_id_list)
        )
        .filter(ProcurementRequestItem.is_deleted.is_(False))
        .all()
    )

    for index, item in enumerate(items):
        try:

            statement = insert(RFQItem).values(
                rfq_id=rfq_id,
                item_id=item.item_id,
                line_number=(index + 1),
                procurement_request_id=item.procurement_request_id,
            )
            session.execute(statement)
            session.commit()

            app_logger.info(
                f"Added to rfq_items :: rfq_id: {rfq_id}, " +
                f"procurement_request_id: {item.procurement_request_id}, " +
                "item_id: {item_id}"
            )

        except Exception as e:
            session.rollback()
            error_logger.error(f"Failed to add RFQ Item :: {e}, data: {item}")

            failed_item_ids.append(item.item_id)
            continue
    
    return failed_item_ids
