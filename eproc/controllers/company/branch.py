from http import HTTPStatus
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from typing import List, Optional, Tuple

from eproc.models.companies.branches import Branch
from eproc.schemas.companies.branches import BranchAutoSchema


class BranchController:
    def __init__(self):
        self.schema = BranchAutoSchema()
        self.many_schema = BranchAutoSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            Branch.query
            .filter(Branch.is_deleted.is_(False))
            .order_by(Branch.description)
        )

        if id_list:
            query = query.filter(Branch.id.in_(id_list))
        
        if search_query:
            query = (
                query
                .filter(or_(
                    Branch.id.ilike(f"%{search_query}%"),
                    Branch.description.ilike(f"%{search_query}%"),
                ))
            )
        
        total = query.count()
        
        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)
        
        results: List[Branch] = query.all()

        if not results:
            return (
                HTTPStatus.NOT_FOUND,
                "Branch tidak ditemukan.",
                [],
                total
            )
        user_data_list = self.many_schema.dump(results)

        return (
            HTTPStatus.OK,
            "Branch ditemukan.",
            user_data_list,
            total
        )
