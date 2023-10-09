from http import HTTPStatus
from sqlalchemy import or_
from traceback import format_exc
from typing import List, Optional, Tuple

from eproc import error_logger
from eproc.models.procurement_requests import ProcurementRequest
from eproc.schemas.procurement_requests import ProcurementRequestAutoSchema


class ProcurementRequestController:
    def __init__(self):
        self.schema = ProcurementRequestAutoSchema()
        self.many_schema = ProcurementRequestAutoSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            ProcurementRequest.query
            .filter(ProcurementRequest.is_deleted.is_(False))
            .order_by(ProcurementRequest.transaction_date.desc())
        )

        if id_list:
            query = (
                query
                .filter(ProcurementRequest.id.in_(id_list))
            )

        if search_query:
            query = (
                query
                .filter(or_(
                    ProcurementRequest.id.ilike(f"%{search_query}%"),
                ))
            )

        total = query.count()

        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)

        item_list: List[ProcurementRequest] = query.all()
        if not item_list:
            return (
                HTTPStatus.NOT_FOUND,
                "Procurement Request tidak ditemukan.",
                [],
                total,
            )
        item_data_list = self.many_schema.dump(item_list)

        return (
            HTTPStatus.OK,
            "Procurement Request ditemukan.",
            item_data_list,
            total,
        )
