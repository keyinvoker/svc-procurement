from http import HTTPStatus
from sqlalchemy import or_
from traceback import format_exc
from typing import List, Optional, Tuple

from eproc import error_logger
from eproc.models.items.procurement_request_items import ProcurementRequestItem
from eproc.models.procurement_requests import ProcurementRequest
from eproc.schemas.procurement_requests import ProcurementRequestAutoSchema
from eproc.schemas.items.procurement_request_items import ProcurementRequestItemAutoSchema


class ProcurementRequestController:
    def __init__(self):
        self.schema = ProcurementRequestAutoSchema()
        self.many_schema = ProcurementRequestAutoSchema(many=True)
    
    def get_detail(self, id: int) -> Tuple[HTTPStatus, str, Optional[dict]]:
        try:
            query = (
                ProcurementRequest.query
                .filter(ProcurementRequest.id == id)
                .filter(ProcurementRequest.is_deleted.is_(False))
            )
            result = query.first()
            if not result:
                return (
                    HTTPStatus.NOT_FOUND,
                    "Data detail PR tidak ditemukan.",
                    data
                )

            data = self.schema.dump(result)
            return (
                HTTPStatus.OK,
                "Data detail PR ditemukan.",
                data
            )

        except Exception as e:
            error_logger.error(f"Error on PRController:get_detail :: {e}, {format_exc()}")
            return (
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "Terjadi kesalahan saat mengambil data detail PR.",
                None
            )

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
    
    def get_items(
        self, procurement_request_id: int
    ) -> Tuple[HTTPStatus, str, Optional[List[dict]], int]:

        query = (
            ProcurementRequestItem.query
            .filter(ProcurementRequestItem.procurement_request_id == procurement_request_id)
            .filter(ProcurementRequestItem.is_deleted.is_(False))
            .order_by(ProcurementRequestItem.lnnum)
        )

        total = query.count()
        if total == 0:
            return (
                HTTPStatus.NOT_FOUND,
                f"Tidak ditemukan barang dari PR dengan id: {procurement_request_id}.",
                None,
                0
            )

        results = query.all()
        data = ProcurementRequestItemAutoSchema(many=True).dump(results)

        return (
            HTTPStatus.OK,
            f"Ditemukan barang dari PR dengan id: {procurement_request_id}.",
            data,
            total
        )
