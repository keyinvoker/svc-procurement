from http import HTTPStatus
from sqlalchemy import or_
from traceback import format_exc
from typing import List, Optional, Tuple

from eproc import error_logger
from eproc.models.vendors.vendors import Vendor
from eproc.schemas.vendors.vendors import (
    VendorAutoSchema,
    VendorDetailAutoSchema,
)


class VendorController:
    def __init__(self):
        self.schema = VendorAutoSchema()
        self.many_schema = VendorAutoSchema(many=True)
        self.detail_schema = VendorDetailAutoSchema()

    def get_detail(self, id: str) -> Tuple[HTTPStatus, str, Optional[dict]]:

        vendor: Vendor = (
            Vendor.query
            .filter(Vendor.id == id)
            .filter(Vendor.is_deleted.is_(False))
            .first()
        )

        if not vendor:
            return (
                HTTPStatus.NOT_FOUND,
                "Vendor tidak ditemukan.",
                None
            )

        vendor_data = self.detail_schema.dump(vendor)

        return (
            HTTPStatus.OK,
            "Vendor ditemukan.",
            vendor_data
        )

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[int] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: int = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        vendor_query = Vendor.query.filter(Vendor.is_deleted.is_(False))

        if id_list:
            vendor_query = (
                vendor_query
                .filter(Vendor.id.in_(id_list))
            )

        if search_query:
            vendor_query = (
                vendor_query
                .filter(or_(
                    Vendor.id.ilike(f"%{search_query}%"),
                    Vendor.name.ilike(f"%{search_query}%"),
                    Vendor.service_type.ilike(f"%{search_query}%"),
                    Vendor.service_description.ilike(f"%{search_query}%"),
                ))
            )

        total = vendor_query.count()

        if limit:
            vendor_query = vendor_query.limit(limit)

        if offset > 0:
            vendor_query = vendor_query.offset(offset)

        item_list: List[Vendor] = vendor_query.all()
        if not item_list:
            return (
                HTTPStatus.NOT_FOUND,
                "Vendor tidak ditemukan.",
                [],
                total,
            )
        item_data_list = self.many_schema.dump(item_list)

        return (
            HTTPStatus.OK,
            "Vendor ditemukan.",
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

                existing_item: Vendor = (
                    Vendor.query
                    .filter(Vendor.category == category)
                    .filter(Vendor.name == name)
                )
                if existing_item:
                    existing_item_list.append(dict(
                        id=existing_item.id,
                        name=existing_item.name,
                    ))
                    continue

                item = Vendor(
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
                error_logger.error(f"Error on VendorController:insert :: {e}, {format_exc()}")
                continue
        
        if new_item_list:
            http_status = HTTPStatus.OK
            message = "Vendor baru berhasil ditambahkan."
        elif existing_item_list:
            http_status = HTTPStatus.CONFLICT
            message = "Vendor gagal ditambahkan karena sudah ada."

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

        item: Vendor = (
            Vendor.query
            .filter(Vendor.id == item_id)
            .filter(Vendor.is_deleted.is_(False))
            .first()
        )
        if not item:
            return HTTPStatus.NOT_FOUND, "Vendor tidak ditemukan."
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

    def delete(self, id_list: List[int]) -> Tuple[HTTPStatus, str]:
        item_list: List[Vendor] = (
            Vendor.query
            .filter(Vendor.id.in_(id_list))
            .filter(Vendor.is_deleted.is_(False))
            .all()
        )
        if not item_list:
            return HTTPStatus.NOT_FOUND, "Vendor tidak ditemukan."

        item_data_list = self.many_schema.dump(item_list)
        try:
            Vendor.bulk_delete(item_data_list)
            return HTTPStatus.OK, "Vendor berhasil dihapus."
        except Exception as e:
            error_logger.error(f"Error on VendorController:delete() :: {e}, {format_exc()}")
            return HTTPStatus.BAD_REQUEST, "Vendor gagal dihapus."
