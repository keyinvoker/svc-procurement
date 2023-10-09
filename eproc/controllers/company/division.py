from http import HTTPStatus
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from typing import List, Optional, Tuple

from eproc.models.companies.divisions import Division
from eproc.schemas.companies.divisions import DivisionAutoSchema


class DivisionController:
    def __init__(self):
        self.schema = DivisionAutoSchema()
        self.many_schema = DivisionAutoSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            Division.query
            .filter(Division.is_deleted.is_(False))
            .order_by(Division.description)
        )

        if id_list:
            query = query.filter(Division.id.in_(id_list))
        
        if search_query:
            query = (
                query
                .filter(or_(
                    Division.id.ilike(f"%{search_query}%"),
                    Division.description.ilike(f"%{search_query}%"),
                ))
            )
        
        total = query.count()
        
        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)
        
        result_list: List[Division] = query.all()

        if not result_list:
            return (
                HTTPStatus.NOT_FOUND,
                "Division tidak ditemukan.",
                [],
                total
            )
        user_data_list = self.many_schema.dump(result_list)

        return (
            HTTPStatus.OK,
            "Division ditemukan.",
            user_data_list,
            total
        )
