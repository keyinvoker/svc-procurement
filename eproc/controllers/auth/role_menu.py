from http import HTTPStatus
from typing import List, Optional, Tuple

from eproc.models.auth.roles_menus import RoleMenu
from eproc.schemas.auth.roles_menus import RoleMenuSchema


class RoleMenuController:
    def __init__(self, **kwargs):
        self.schema = RoleMenuSchema()
        self.many_schema = RoleMenuSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        role_id_list: List[str] = kwargs.get("role_id_list")
        menu_id_list: List[str] = kwargs.get("menu_id_list")
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            RoleMenu.query
            .filter(RoleMenu.is_deleted.is_(False))
            .order_by(
                RoleMenu.role_id,
                RoleMenu.menu_id,
            )
        )

        if role_id_list:
            query = query.filter(RoleMenu.role_id.in_(role_id_list))

        if menu_id_list:
            query = query.filter(RoleMenu.menu_id.in_(menu_id_list))

        total = query.count()

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        results: List[RoleMenu] = query.all()
        if not results:
            return (
                HTTPStatus.NOT_FOUND,
                "Role menu tidak ditemukan.",
                [],
                total,
            )

        data = self.many_schema.dump(results)

        return (
            HTTPStatus.OK,
            "Role menu ditemukan.",
            data,
            total
        )
