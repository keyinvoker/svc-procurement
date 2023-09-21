from os import getenv
from typing import Optional, Union


class Env:
    def string(self, value: str, default: Optional[str] = None) -> str:
        value =  getenv(value, default)
        return str(value)

    def int(self, value: str, default: Optional[str] = None) -> int:
        value =  getenv(value, default)
        return int(value)

    def bool(self, value: Union[str, bool], default: Optional[str] = None) -> bool:
        if isinstance(value, bool):
            return value

        value =  getenv(value, default)
        if (
            isinstance(value, str) and
            value.lower() in ["true", "t", "1"]
        ):
            return True
        return False
