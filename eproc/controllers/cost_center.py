from http import HTTPStatus
from typing import Optional, Tuple

from eproc.models.cost_centers import CostCenter
from eproc.schemas.cost_centers import (
    CostCenterAutoSchema,
)


class CostCenterController:
    def __init__(self, **kwargs):
        self.schema = CostCenterAutoSchema()
        self.many_schema = CostCenterAutoSchema(many=True)
    
    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, Optional[dict]]:

        result = (
            CostCenter.query
            .filter(CostCenter.is_deleted.is_(False))
            .all()
        )
        if not result:
            return (
                HTTPStatus.NOT_FOUND,
                "Data cost center kosong.",
                None
            )

        data = self.many_schema.dump(result)

        return HTTPStatus.OK, "Data cost center ditemukan.", data
