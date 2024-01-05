from http import HTTPStatus
from traceback import format_exc
from typing import List, Optional, Tuple

from eproc import error_logger
from eproc.models.cost_centers import CostCenter
from eproc.models.items.items import Item
from eproc.models.items.item_categories import ItemCategory
from eproc.models.items.item_classes import ItemClass
from eproc.models.items.procurement_request_items import ProcurementRequestItem
from eproc.schemas.items.items import (
    ItemAutoSchema,
    ItemCategoryAutoSchema,
    ItemClassAutoSchema,
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
            .with_entities(
                Item.id,
                Item.description,
                Item.item_category_id,
                ItemCategory.description.label("item_category_description"),
                ItemCategory.item_class_id,
                ItemClass.description.label("item_class_description"),
                Item.unit_of_measurement,
                Item.minimum_quantity,
                Item.cost_center_id,
                CostCenter.description.label("cost_center_description"),
                Item.sla,
                Item.tags,
                Item.is_active,
                Item.created_at,
                Item.updated_at,
                Item.updated_by,
                ProcurementRequestItem.required_days_interval
            )
            .join(
                ItemCategory,
                ItemCategory.id == Item.item_category_id
            )
            .join(
                ItemClass,
                ItemClass.id == ItemCategory.item_class_id
            )
            .join(
                CostCenter,
                CostCenter.id == ItemCategory.cost_center_id
            )
            .outerjoin(
                ProcurementRequestItem,
                ProcurementRequestItem.item_id == Item.id
            )
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

    def get_classes(
        self
    ) -> Tuple[HTTPStatus, str, Optional[List[dict]]]:
        return (
            HTTPStatus.OK,
            "Kelas Barang ditemukan.",
            ItemClassAutoSchema(many=True).dump(
                ItemClass.query
                .filter(
                    ItemClass.is_active.is_(True),
                    ItemClass.is_deleted.is_(False),
                )
                .all()
            )
        )
    
    def get_categories(
        self,
        item_class_id: str
    ) -> Tuple[HTTPStatus, str, Optional[List[dict]]]:

        query = (
            ItemCategory.query
            .filter(
                ItemCategory.is_active.is_(True),
                ItemCategory.is_deleted.is_(False),
            )
        )

        if item_class_id:
            additional_error_message = f" dengan id Kelas Barang: {item_class_id}"

            query = (
                query
                .filter(
                    ItemCategory.item_class_id == item_class_id,
                )
            )

        results = query.all()
        if not results:
            return (
                HTTPStatus.NOT_FOUND,
                f"Tidak ditemukan Kategori Barang{additional_error_message}.",
                None
            )
        
        data = self.category_many_schema.dump(results)
        return (
            HTTPStatus.OK,
            "Data Kategori Barang ditemukan.",
            data
        )
    
    def add_item(self, **kwargs) -> Tuple[HTTPStatus, str]:

        id = kwargs.get("id")
        description = kwargs.get("description")
        unit_of_measurement = kwargs.get("unit_of_measurement")
        cost_center_id = kwargs.get("cost_center_id")
        minimum_quantity = kwargs.get("minimum_quantity")
        item_category_id = kwargs.get("item_category_id")
        sla = kwargs.get("sla")
        is_adjustable = kwargs.get("is_adjustable")
        is_active = kwargs.get("is_active")
        updated_by = kwargs.get("updated_by")

        item = (
            Item.query
            .filter(Item.id == id)
            .first()
        )
        if item:
            return (
                HTTPStatus.CONFLICT,
                f"Sudah ada item dengan id: {id}."
            )
        
        new_item = Item(
            id=id,
            description=description,
            unit_of_measurement=unit_of_measurement,
            cost_center_id=cost_center_id,
            minimum_quantity=minimum_quantity,
            item_category_id=item_category_id,
            sla=sla,
            updated_by=updated_by,
        )

        if is_adjustable is not None:
            new_item.is_adjustable = is_adjustable

        if is_active is not None:
            new_item.is_active = is_active
        
        try:
            new_item.save()

            return (
                HTTPStatus.CREATED,
                "Item berhasil dibuat."
            )
        except Exception as e:
            error_logger.error(f"Error on ItemController:add_item() :: {e}, {format_exc()}")

            return (
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "Terjasi kesalahan saat membuat item."
            )
