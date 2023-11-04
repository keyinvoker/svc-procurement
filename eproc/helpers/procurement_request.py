from sqlalchemy.sql import func

from eproc.models.procurement_requests import ProcurementRequest


def get_latest_sequence_number(year: int, month: int) -> int:
    latest_sequence_number = func.coalesce(
        func.max(ProcurementRequest.sequence_number), 0
    ).label("latest_sequence_number")

    sequence = (
        ProcurementRequest.query
        .with_entities(latest_sequence_number)
        .filter(
            ProcurementRequest.year == year,
            ProcurementRequest.month == month,
        )
        .first()
    )

    return sequence[0]


def get_next_sequence_number(year: int, month: int) -> int:
    return get_latest_sequence_number(year, month) + 1
