from http import HTTPStatus
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from typing import List, Optional, Tuple

from eproc.models.references import Reference
from eproc.models.auth.roles import Role
from eproc.schemas.auth.roles import RoleAutoSchema


class RoleController:
    def __init__(self):
        self.schema = RoleAutoSchema()
        self.many_schema = RoleAutoSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: int = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        role_query = (
            Role.query
            .filter(Role.is_deleted.is_(False))
            .order_by(Role.description)
        )

        if id_list:
            role_query = role_query.filter(Role.id.in_(id_list))
        
        if search_query:
            role_query = (
                role_query
                .filter(or_(
                    Role.id.ilike(f"%{search_query}%"),
                    Role.description.ilike(f"%{search_query}%"),
                ))
            )
        
        total = role_query.count()
        
        if limit:
            role_query = role_query.limit(limit)

        if offset > 0:
            role_query = role_query.offset(offset)
        
        role_list: List[Role] = role_query.all()

        if not role_list:
            return (
                HTTPStatus.NOT_FOUND,
                "Role tidak ditemukan.",
                [],
                total
            )
        user_data_list = self.many_schema.dump(role_list)

        return (
            HTTPStatus.OK,
            "Role ditemukan.",
            user_data_list,
            total
        )
