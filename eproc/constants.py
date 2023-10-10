from sqlalchemy.sql import func
from typing import List

from eproc.models.auth.roles import Role

ALL_ROLE_ID_LIST: List[str] = Role.query.with_entities(func.array_agg(Role.id)).first()[0]
