from http import HTTPStatus
from sqlalchemy import or_
from sqlalchemy.sql import func
from typing import List, Optional, Tuple

from eproc.models.companies.branches import Branch
from eproc.models.items.items import Item
from eproc.models.purchase_orders.purchase_orders import PurchaseOrder
from eproc.models.purchase_orders.purchase_order_items import PurchaseOrderItem
from eproc.models.references import Reference
from eproc.models.users.users import User
from eproc.models.vendors.vendors import Vendor
from eproc.schemas.purchase_orders.purchase_orders import (
    PurchaseOrderAutoSchema,
    PurchaseOrderItemAutoSchema,
)


class PurchaseOrderController:
    def __init__(self):
        self.schema = PurchaseOrderAutoSchema()
        self.many_schema = PurchaseOrderAutoSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            PurchaseOrder.query
            .with_entities(
                PurchaseOrder.id,
                PurchaseOrder.fcoid,
                PurchaseOrder.vendor_id,
                Vendor.name.label("vendor_name"),
                Vendor.first_address.label("vendor_address"),
                PurchaseOrder.reference_id,
                Reference.description.label("reference_description"),
                User.full_name.label("updated_by"),
                PurchaseOrder.transaction_type,
                PurchaseOrder.transaction_date,
                PurchaseOrder.document_number,
                PurchaseOrder.purchase_order_type,
                PurchaseOrder.currency,
                PurchaseOrder.description,
                PurchaseOrder.app_source,
                PurchaseOrder.prtno,
                PurchaseOrder.discount,
                PurchaseOrder.tax_percentage,
                PurchaseOrder.payment_time,
                PurchaseOrder.payment_period,
                PurchaseOrder.payment_note,
                PurchaseOrder.sequence_number,
                PurchaseOrder.dref1,
                PurchaseOrder.dref2,
                PurchaseOrder.dref3,
                PurchaseOrder.flag1,
                PurchaseOrder.flag2,
                PurchaseOrder.temps,
            )
            .join(Reference, Reference.id == PurchaseOrder.reference_id)
            .join(User, User.id == PurchaseOrder.updated_by)
            .outerjoin(Vendor, Vendor.id == PurchaseOrder.vendor_id)
            .filter(PurchaseOrder.is_deleted.is_(False))
            .order_by(PurchaseOrder.transaction_date.desc())
        )

        if id_list:
            query = (
                query
                .filter(PurchaseOrder.id.in_(id_list))
            )

        if search_query:
            query = (
                query
                .filter(or_(
                    PurchaseOrder.id.ilike(f"%{search_query}%"),
                ))
            )

        total = query.count()

        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)

        item_list: List[PurchaseOrder] = query.all()
        if not item_list:
            return (
                HTTPStatus.NOT_FOUND,
                "PO tidak ditemukan.",
                [],
                total,
            )
        item_data_list = self.many_schema.dump(item_list)

        return (
            HTTPStatus.OK,
            "PO ditemukan.",
            item_data_list,
            total,
        )
    
    def get_detail(self, id: int) -> Tuple[HTTPStatus, str, Optional[dict]]:
        result = (
            PurchaseOrder.query
            .with_entities(
                PurchaseOrder.id,
                PurchaseOrder.fcoid.label("branch_id"),
                Branch.description.label("branch_location"),
                Branch.first_address.label("branch_address"),
                PurchaseOrder.vendor_id,
                Vendor.name.label("vendor_name"),
                Vendor.first_address.label("vendor_address"),
                PurchaseOrder.reference_id,
                Reference.description.label("reference_description"),
                User.full_name.label("updated_by"),
                PurchaseOrder.transaction_type,
                PurchaseOrder.transaction_date,
                PurchaseOrder.document_number,
                PurchaseOrder.purchase_order_type,
                PurchaseOrder.currency,
                PurchaseOrder.description,
                PurchaseOrder.app_source,
                PurchaseOrder.prtno,
                PurchaseOrder.discount,
                PurchaseOrder.tax_percentage,
                PurchaseOrder.payment_time,
                PurchaseOrder.payment_period,
                PurchaseOrder.payment_note,
                PurchaseOrder.sequence_number,
                PurchaseOrder.dref1,
                PurchaseOrder.dref2,
                PurchaseOrder.dref3,
                PurchaseOrder.flag1,
                PurchaseOrder.flag2,
                PurchaseOrder.temps,
            )
            .outerjoin(Vendor, Vendor.id == PurchaseOrder.vendor_id)
            .outerjoin(Reference, Reference.id == PurchaseOrder.reference_id)
            .outerjoin(User, User.id == PurchaseOrder.updated_by)
            .outerjoin(Branch, Branch.id == PurchaseOrder.fcoid)
            .filter(
                PurchaseOrder.id == id,
                PurchaseOrder.is_deleted.is_(False),
            )
            .first()
        )

        if not result:
            return (
                HTTPStatus.NOT_FOUND,
                f"Tidak ditemukan detail PO dengan ID: {id}",
                None
            )
        
        return (
            HTTPStatus.OK,
            f"Ditemukan detail PO.",
            self.schema.dump(result)
        )
    
    def get_items(
        self, **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:
        purchase_order_id = kwargs.get("purchase_order_id")
        limit = kwargs.get("limit")
        offset = kwargs.get("offset")

        (
            total_amount,
            total_discount_amount,
            total_net_price,
            total_tax_amount,
            total_net_amount,
        ) = (
            PurchaseOrderItem.query
            .with_entities(
                func.sum(PurchaseOrderItem.amount).label("total_amount"),
                func.sum(PurchaseOrderItem.discount_amount).label("total_discount_amount"),
                func.sum(PurchaseOrderItem.net_price).label("total_net_price"),
                func.sum(PurchaseOrderItem.tax_amount).label("total_tax_amount"),
                func.sum(PurchaseOrderItem.net_amount).label("total_net_amount"),
            )
            .filter(PurchaseOrderItem.purchase_order_id == purchase_order_id)
            .filter(PurchaseOrderItem.is_deleted.is_(False))
            .first()
        )

        query = (
            PurchaseOrderItem.query
            .with_entities(
                PurchaseOrderItem.line_number,
                PurchaseOrderItem.purchase_order_id,
                PurchaseOrderItem.item_id,
                Item.description.label("item_name"),
                Item.unit_of_measurement,
                PurchaseOrderItem.item_quantity,
                PurchaseOrderItem.price,
                PurchaseOrderItem.amount,
                PurchaseOrderItem.discount_amount,
                PurchaseOrderItem.tax_amount,
                PurchaseOrderItem.net_amount,
                PurchaseOrderItem.net_price,
                PurchaseOrderItem.required_date,
            )
            .outerjoin(Item, Item.id == PurchaseOrderItem.item_id)
            .filter(PurchaseOrderItem.purchase_order_id == purchase_order_id)
            .filter(PurchaseOrderItem.is_deleted.is_(False))
            .order_by(PurchaseOrderItem.line_number)
        )

        total = query.count()
        if total == 0:
            return (
                HTTPStatus.NOT_FOUND,
                f"Tidak ditemukan barang dari PO dengan id: {purchase_order_id}.",
                [],
                0
            )
        
        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        results = query.all()
        print(results)
        data = PurchaseOrderItemAutoSchema(many=True).dump(results)

        return (
            HTTPStatus.OK,
            f"Ditemukan barang dari PO dengan id: {purchase_order_id}.",
            data,
            float(total_amount),
            float(total_discount_amount),
            float(total_net_price),
            float(total_tax_amount),
            float(total_net_amount),
            total
        )
