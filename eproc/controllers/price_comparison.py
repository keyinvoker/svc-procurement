from http import HTTPStatus
from sqlalchemy import or_
from traceback import format_exc
from typing import List, Optional, Tuple

from eproc import error_logger
from eproc.models.price_comparisons import PriceComparison
from eproc.schemas.price_comparisons import PriceComparisonAutoSchema


class PriceComparisonController:
    def __init__(self):
        self.schema = PriceComparisonAutoSchema()
        self.many_schema = PriceComparisonAutoSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            PriceComparison.query
            .filter(PriceComparison.is_deleted.is_(False))
            .order_by(PriceComparison.transaction_date.desc())
        )

        if id_list:
            query = (
                query
                .filter(PriceComparison.id.in_(id_list))
            )

        if search_query:
            query = (
                query
                .filter(or_(
                    PriceComparison.id.ilike(f"%{search_query}%"),
                ))
            )

        total = query.count()

        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)

        item_list: List[PriceComparison] = query.all()
        if not item_list:
            return (
                HTTPStatus.NOT_FOUND,
                "Perbandingan harga vendor tidak ditemukan.",
                [],
                total,
            )
        item_data_list = self.many_schema.dump(item_list)

        return (
            HTTPStatus.OK,
            "Perbandingan harga vendor ditemukan.",
            item_data_list,
            total,
        )
