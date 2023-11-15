from datetime import datetime
from pytz import timezone
from sqlalchemy.sql import func
from typing import Dict, List

from eproc import db


def split_string_into_list(
    data: Dict[str, str],
    list_data_keys: List[str]
) -> dict:

    for key in list_data_keys:
        if key in data:
            data[key] = data[key].split(",")

    return data


def wibnow() -> datetime:
    return datetime.now(timezone("Asia/Jakarta")).replace(tzinfo=None)


def get_latest_sequence_number(
    model: db.Model,
    year: int,
    month: int
) -> int:

    latest_sequence_number = func.coalesce(
        func.max(model.sequence_number), 0
    ).label("latest_sequence_number")

    sequence = (
        model.query
        .with_entities(latest_sequence_number)
        .filter(
            model.year == year,
            model.month == month,
        )
        .first()
    )

    return sequence[0]


def get_next_sequence_number(
    model: db.Model,
    year: int,
    month: int
) -> int:
    return get_latest_sequence_number(model, year, month) + 1
