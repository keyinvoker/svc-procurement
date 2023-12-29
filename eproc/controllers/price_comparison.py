from http import HTTPStatus
from sqlalchemy import or_
from typing import List, Optional, Tuple

from eproc.models.price_comparisons import PriceComparison
from eproc.models.references import Reference
from eproc.models.users.users import User
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
            .with_entities(
                PriceComparison.id,
                PriceComparison.rfq_id,
                PriceComparison.reference_id,
                Reference.description.label("reference_description"),
                PriceComparison.document_number,
                PriceComparison.transaction_date,
                PriceComparison.transaction_type,
                PriceComparison.year,
                PriceComparison.month,
                PriceComparison.description,
                PriceComparison.app_source,
                PriceComparison.prtno,
                PriceComparison.recom,
                PriceComparison.plfon,
                PriceComparison.sequence_number,
                PriceComparison.flag1,
                PriceComparison.flag2,
                PriceComparison.dref1,
                PriceComparison.dref2,
                PriceComparison.dref3,
                PriceComparison.temps,
                PriceComparison.created_at,
                User.full_name.label("updated_by"),
                PriceComparison.updated_at,
            )
            .join(User, User.id == PriceComparison.updated_by)
            .join(Reference, Reference.id == PriceComparison.reference_id)
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
