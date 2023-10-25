from http import HTTPStatus
from sqlalchemy import or_
from traceback import format_exc
from typing import List, Optional, Tuple

from eproc import error_logger
from eproc.models.items.items import Item
from eproc.models.items.item_categories import ItemCategory
from eproc.schemas.items.items import (
    ItemAutoSchema,
    ItemCategoryAutoSchema,
)


class ItemController:
    def __init__(self):
        self.schema = ItemAutoSchema()
        self.many_schema = ItemAutoSchema(many=True)

        self.category_schema = ItemCategoryAutoSchema()
        self.category_many_schema = ItemCategoryAutoSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        item_category_id: str = kwargs.get("item_category_id")
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            Item.query
            .filter(
                Item.is_active.is_(True),
                Item.is_deleted.is_(False),
            )
            .order_by(Item.id)
        )

        if id_list:
            query = query.filter(Item.id.in_(id_list))
        
        if item_category_id:
            query = query.filter(
                Item.item_category_id == item_category_id
            )

        total = query.count()

        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)

        results: List[Item] = query.all()
        if not results:
            return (
                HTTPStatus.NOT_FOUND,
                "Barang tidak ditemukan.",
                [],
                total,
            )

        data_list = self.many_schema.dump(results)

        return (
            HTTPStatus.OK,
            "Barang ditemukan.",
            data_list,
            total,
        )
    
    def get_categories(
        self,
        item_class_id: str
    ) -> Tuple[HTTPStatus, str, Optional[List[dict]]]:

        results = (
            ItemCategory.query
            .filter(
                ItemCategory.item_class_id == item_class_id,
                ItemCategory.is_active.is_(True),
                ItemCategory.is_deleted.is_(False),
            )
            .all()
        )
        if not results:
            return (
                HTTPStatus.NOT_FOUND,
                f"Tidak ditemukan Kategori Barang dengan id Kelas Barang: {item_class_id}."
            )
        
        data = self.category_many_schema.dump(results)
        return (
            HTTPStatus.OK,
            "Data Kategori Barang ditemukan.",
            data
        )
