from http import HTTPStatus
from typing import List, Optional, Tuple

from eproc import error_logger
from eproc.models.auth.menus import Menu
from eproc.schemas.auth.menus import MenuSchema


class MenuController:
    def __init__(self, **kwargs):
        self.schema = MenuSchema()
        self.many_schema = MenuSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            Menu.query
            .filter(Menu.is_deleted.is_(False))
        )

        if id_list:
            query = query.filter(Menu.id.in_(id_list))
        
        total = query.count()

        if limit:
            query = query.limit(limit)
        
        if offset:
            query = query.offset(offset)

        results: List[Menu] = query.all()
        if not results:
            return (
                HTTPStatus.NOT_FOUND,
                "Menu tidak ditemukan.",
                [],
                total,
            )

        data = self.many_schema.dump(results)

        return (
            HTTPStatus.OK,
            "Menu ditemukan.",
            data,
            total
        )
    
    def get_detail(self, id: str):
        menu: Menu = (
            Menu.query
            .filter(
                Menu.id == id,
                Menu.is_deleted.is_(False),
            )
            .first()
        )
        if not menu:
            return (
                HTTPStatus.NOT_FOUND,
                "Menu tidak ditemukan.",
                None,
            )

        data = self.schema.dump(menu)

        return (
            HTTPStatus.OK,
            "Detail menu ditemukan.",
            data,
        )
