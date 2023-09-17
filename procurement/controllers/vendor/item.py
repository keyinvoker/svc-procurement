from http import HTTPStatus
from sqlalchemy import or_
from traceback import format_exc
from typing import List, Tuple

from procurement import error_logger
from procurement.models.vendors.items import Item
from procurement.schemas.vendors.items import ItemAutoSchema


class ItemController:
    def __init__(self):
        self.schema = ItemAutoSchema()
        self.many_schema = ItemAutoSchema(many=True)

    def get_list(self, **kwargs) -> Tuple[HTTPStatus, str, List[dict], int]:
        item_id_list: List[int] = kwargs.get("item_id_list")
        category_list: List[str] = kwargs.get("category_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: int = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        item_query = Item.query.filter(Item.is_deleted.is_(False))

        if item_id_list:
            item_query = (
                item_query
                .filter(Item.id.in_(item_id_list))
            )

        if category_list:
            item_query = (
                item_query
                .filter(Item.category.in_(category_list))
            )

        if search_query:
            item_query = (
                item_query
                .filter(or_(
                    Item.category.ilike(f"%{search_query}%"),
                    Item.name.ilike(f"%{search_query}%"),
                    Item.description.ilike(f"%{search_query}%"),
                ))
            )

        total = item_query.count()

        if limit:
            item_query = item_query.limit(limit)

        if offset > 0:
            item_query = item_query.offset(offset)

        item_list: List[Item] = item_query.all()
        if not item_list:
            return (
                HTTPStatus.NOT_FOUND,
                "Barang tidak ditemukan.",
                [],
                total,
            )
        item_data_list = self.many_schema.dump(item_list)

        return (
            HTTPStatus.OK,
            "Barang ditemukan.",
            item_data_list,
            total,
        )

    def insert(self, payload_list: List[dict]) -> Tuple[HTTPStatus, str, dict]:
        new_item_list: List[dict] = list()
        existing_item_list: List[dict] = list()
    
        for payload in payload_list:
            try:
                category = payload.get("category")
                name = payload.get("name")
                description = payload.get("description")

                existing_item: Item = (
                    Item.query
                    .filter(Item.category == category)
                    .filter(Item.name == name)
                )
                if existing_item:
                    existing_item_list.append(dict(
                        id=existing_item.id,
                        name=existing_item.name,
                    ))
                    continue

                item = Item(
                    category=category,
                    name=name,
                    description=description,
                )
                item.save()

                new_item_list.append(dict(
                    id=item.id,
                    name=item.name,
                ))
            except Exception as e:
                error_logger.error(f"Error on ItemController:insert :: {e}, {format_exc()}")
                continue
        
        if new_item_list:
            http_status = HTTPStatus.OK
            message = "Barang baru berhasil ditambahkan."
        elif existing_item_list:
            http_status = HTTPStatus.CONFLICT
            message = "Barang gagal ditambahkan karena sudah ada."

        data = dict(
            new_item_list=new_item_list,
            existing_item_list=existing_item_list,
        )

        return http_status, message, data

    def update(self, **kwargs) -> Tuple[HTTPStatus, str]:
        item_id: int = kwargs.get("item_id")
        category: str = kwargs.get("category")
        name: str = kwargs.get("name")
        description: str = kwargs.get("description")

        item: Item = (
            Item.query
            .filter(Item.id == item_id)
            .filter(Item.is_deleted.is_(False))
            .first()
        )
        if not item:
            return HTTPStatus.NOT_FOUND, "Barang tidak ditemukan."
        elif (
            not category
            and not name
            and not description
        ):
            return (
                HTTPStatus.BAD_REQUEST,
                "Data barang sama dan tidak perlu diperbarui."
            )

        if category:
            item.category = category

        if name:
            item.name = name

        if description:
            item.description = description

        item.save()

        return HTTPStatus.OK, "Data barang berhasil diperbarui."

    def delete(self, item_id_list: List[int]) -> Tuple[HTTPStatus, str]:
        item_list: List[Item] = (
            Item.query
            .filter(Item.id.in_(item_id_list))
            .filter(Item.is_deleted.is_(False))
            .all()
        )
        if not item_list:
            return HTTPStatus.NOT_FOUND, "Barang tidak ditemukan."

        item_data_list = self.many_schema.dump(item_list)
        try:
            Item.bulk_delete(item_data_list)
            return HTTPStatus.OK, "Barang berhasil dihapus."
        except Exception as e:
            error_logger.error(f"Error on ItemController:delete() :: {e}, {format_exc()}")
            return HTTPStatus.BAD_REQUEST, "Barang gagal dihapus."
