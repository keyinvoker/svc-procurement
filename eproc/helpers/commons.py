from datetime import datetime
from pytz import timezone
from typing import Dict, List


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
