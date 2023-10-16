from http import HTTPStatus
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from typing import List, Optional, Tuple

from eproc.models.companies.departments import Department
from eproc.schemas.companies.departments import DepartmentAutoSchema


class DepartmentController:
    def __init__(self):
        self.schema = DepartmentAutoSchema()
        self.many_schema = DepartmentAutoSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            Department.query
            .filter(Department.is_deleted.is_(False))
            .order_by(Department.description)
        )

        if id_list:
            query = query.filter(Department.id.in_(id_list))
        
        if search_query:
            query = (
                query
                .filter(or_(
                    Department.id.ilike(f"%{search_query}%"),
                    Department.description.ilike(f"%{search_query}%"),
                ))
            )
        
        total = query.count()
        
        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)
        
        results: List[Department] = query.all()

        if not results:
            return (
                HTTPStatus.NOT_FOUND,
                "Department tidak ditemukan.",
                [],
                total
            )
        user_data_list = self.many_schema.dump(results)

        return (
            HTTPStatus.OK,
            "Department ditemukan.",
            user_data_list,
            total
        )
