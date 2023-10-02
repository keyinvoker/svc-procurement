from http import HTTPStatus
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from typing import List, Optional, Tuple

from eproc.models.companies.directorates import Directorate
from eproc.schemas.companies.directorates import DirectorateAutoSchema


class DirectorateController:
    def __init__(self):
        self.schema = DirectorateAutoSchema()
        self.many_schema = DirectorateAutoSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: int = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            Directorate.query
            .filter(Directorate.is_deleted.is_(False))
            .order_by(Directorate.description)
        )

        if id_list:
            query = query.filter(Directorate.id.in_(id_list))
        
        if search_query:
            query = (
                query
                .filter(or_(
                    Directorate.id.ilike(f"%{search_query}%"),
                    Directorate.description.ilike(f"%{search_query}%"),
                ))
            )
        
        total = query.count()
        
        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)
        
        result_list: List[Directorate] = query.all()

        if not result_list:
            return (
                HTTPStatus.NOT_FOUND,
                "Directorate tidak ditemukan.",
                [],
                total
            )
        user_data_list = self.many_schema.dump(result_list)

        return (
            HTTPStatus.OK,
            "Directorate ditemukan.",
            user_data_list,
            total
        )
