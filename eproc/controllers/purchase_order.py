from http import HTTPStatus
from sqlalchemy import or_
from traceback import format_exc
from typing import List, Optional, Tuple

from eproc import error_logger
from eproc.models.purchase_orders.purchase_orders import PurchaseOrder
from eproc.schemas.purchase_orders.purchase_orders import PurchaseOrderAutoSchema


class PurchaseOrderController:
    def __init__(self):
        self.schema = PurchaseOrderAutoSchema()
        self.many_schema = PurchaseOrderAutoSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            PurchaseOrder.query
            .filter(PurchaseOrder.is_deleted.is_(False))
            .order_by(PurchaseOrder.transaction_date.desc())
        )

        if id_list:
            query = (
                query
                .filter(PurchaseOrder.id.in_(id_list))
            )

        if search_query:
            query = (
                query
                .filter(or_(
                    PurchaseOrder.id.ilike(f"%{search_query}%"),
                ))
            )

        total = query.count()

        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)

        item_list: List[PurchaseOrder] = query.all()
        if not item_list:
            return (
                HTTPStatus.NOT_FOUND,
                "PO tidak ditemukan.",
                [],
                total,
            )
        item_data_list = self.many_schema.dump(item_list)

        return (
            HTTPStatus.OK,
            "PO ditemukan.",
            item_data_list,
            total,
        )
