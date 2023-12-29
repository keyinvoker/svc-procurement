from http import HTTPStatus
from sqlalchemy import or_
from typing import List, Optional, Tuple

from eproc.models.purchase_orders.purchase_orders import PurchaseOrder
from eproc.models.references import Reference
from eproc.models.users.users import User
from eproc.models.vendors.vendors import Vendor
from eproc.schemas.purchase_orders.purchase_orders import PurchaseOrderAutoSchema


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
