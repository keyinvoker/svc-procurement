from http import HTTPStatus
from sqlalchemy import or_
from traceback import format_exc
from typing import List, Tuple

from procurement import error_logger
from procurement.models.vendors.items import Item
from procurement.schemas.vendors.items import ItemAutoSchema


class ItemController:
    def __init__(self, **kwargs):
        self.schema = ItemAutoSchema()
        self.many_schema = ItemAutoSchema(many=True)

        self.item_id: int = kwargs.get("item_id")
        self.category: str = kwargs.get("category")
        self.name: str = kwargs.get("name")
        self.description: str = kwargs.get("description")
        self.item_id_list: List[int] = kwargs.get("item_id_list")
        self.category_list: List[str] = kwargs.get("category_list")
        self.search_query: str = kwargs.get("search_query").strip()
        self.limit: int = kwargs.get("limit")
        self.offset: int = kwargs.get("offset")

    def get_list(self) -> Tuple[HTTPStatus, str, List[dict], int]:
        item_query = Item.query.filter(Item.is_deleted.is_(False))

        if self.item_id_list:
            item_query = (
                item_query
                .filter(Item.id.in_(self.item_id_list))
            )

        if self.category_list:
            item_query = (
                item_query
                .filter(Item.category.in_(self.category_list))
            )

        if self.search_query:
            item_query = (
                item_query
                .filter(or_(
                    Item.category.ilike(f"%{self.search_query}%"),
                    Item.name.ilike(f"%{self.search_query}%"),
                    Item.description.ilike(f"%{self.search_query}%"),
                ))
            )

        total = item_query.count()

        if self.limit:
            item_query = item_query.limit(self.limit)

        if self.offset > 0:
            item_query = item_query.offset(self.offset)

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

    def insert(self, data_list: List[dict]) -> Tuple[HTTPStatus, str, dict]:
        new_item_list: List[dict] = list()
        existing_item_list: List[dict] = list()
    
        for data in data_list:
            try:
                category = data.get("category")
                name = data.get("name")
                description = data.get("description")

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

    def update(self) -> Tuple[HTTPStatus, str]:
        item: Item = (
            Item.query
            .filter(Item.id == self.item_id)
            .filter(Item.is_deleted.is_(False))
            .first()
        )
        if not item:
            return HTTPStatus.NOT_FOUND, "Barang tidak ditemukan."
        elif (
            not self.category
            and not self.name
            and not self.description
        ):
            return (
                HTTPStatus.BAD_REQUEST,
                "Data barang sama dan tidak perlu diperbarui."
            )

        if self.category:
            item.category = self.category

        if self.name:
            item.name = self.name

        if self.description:
            item.description = self.description

        item.save()

        return HTTPStatus.OK, "Data barang berhasil diperbarui."

    def delete(self) -> Tuple[HTTPStatus, str]:
        item_list: List[Item] = (
            Item.query
            .filter(Item.id.in_(self.item_id_list))
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
