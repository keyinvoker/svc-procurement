from http import HTTPStatus
from sqlalchemy import or_
from traceback import format_exc
from typing import List, Optional, Tuple

from eproc import error_logger
from eproc.models.links import Link
from eproc.schemas.links import LinkAutoSchema


class LinkController:
    def __init__(self):
        self.schema = LinkAutoSchema()
        self.many_schema = LinkAutoSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            Link.query
            .filter(Link.is_deleted.is_(False))
            .order_by(Link.id)
        )

        if id_list:
            query = (
                query
                .filter(Link.id.in_(id_list))
            )

        total = query.count()

        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)

        results: List[Link] = query.all()
        if not results:
            return (
                HTTPStatus.NOT_FOUND,
                "Tautan tidak ditemukan.",
                [],
                total,
            )
        data_list = self.many_schema.dump(results)

        return (
            HTTPStatus.OK,
            "Tautan ditemukan.",
            data_list,
            total,
        )
