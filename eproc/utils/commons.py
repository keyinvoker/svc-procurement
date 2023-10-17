from datetime import datetime
from pytz import timezone


def wibnow() -> datetime:
    return datetime.now(timezone("Asia/Jakarta")).replace(tzinfo=None)
