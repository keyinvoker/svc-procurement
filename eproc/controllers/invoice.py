from http import HTTPStatus
from typing import List, Optional, Tuple

from eproc.models.invoices import Invoice
from eproc.schemas.invoices import InvoiceSchema


class InvoiceController:
    def __init__(self):
        self.schema = InvoiceSchema()
        self.many_schema = InvoiceSchema(many=True)
    
    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            Invoice.query
            .filter(Invoice.is_deleted.is_(False))
            .order_by(Invoice.id)
        )

        if id_list:
            query = (
                query
                .filter(Invoice.id.in_(id_list))
            )

        total = query.count()

        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)

        results: List[Invoice] = query.all()
        if not results:
            return (
                HTTPStatus.NOT_FOUND,
                "Invoice tidak ditemukan.",
                [],
                total,
            )
        data_list = self.many_schema.dump(results)

        return (
            HTTPStatus.OK,
            "Invoice ditemukan.",
            data_list,
            total,
        )
