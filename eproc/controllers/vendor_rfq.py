from http import HTTPStatus
from sqlalchemy import or_
from typing import List, Optional, Tuple

from eproc.models.references import Reference
from eproc.models.users.users import User
from eproc.models.vendors.vendors import Vendor
from eproc.models.vendor_rfqs import VendorRFQ
from eproc.schemas.vendor_rfqs import VendorRFQAutoSchema


class VendorRFQController:
    def __init__(self):
        self.schema = VendorRFQAutoSchema()
        self.many_schema = VendorRFQAutoSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            VendorRFQ.query
            .with_entities(
                VendorRFQ.id,
                VendorRFQ.vendor_id,
                Vendor.name.label("vendor_name"),
                Vendor.first_address.label("vendor_address"),
                VendorRFQ.branch_id,
                VendorRFQ.reference_id,
                Reference.description.label("reference_description"),
                User.full_name.label("updated_by"),
                VendorRFQ.document_number,
                VendorRFQ.transaction_date,
                VendorRFQ.year,
                VendorRFQ.month,
                VendorRFQ.description,
                VendorRFQ.app_source,
                VendorRFQ.rfqdn,
                VendorRFQ.rfqtn,
                VendorRFQ.pcppn,
                VendorRFQ.paytm,
                VendorRFQ.paypd,
                VendorRFQ.paynt,
                VendorRFQ.sequence_number,
                VendorRFQ.dref1,
                VendorRFQ.dref2,
                VendorRFQ.dref3,
                VendorRFQ.flag1,
                VendorRFQ.flag2,
                VendorRFQ.temps,
            )
            .join(Reference, Reference.id == VendorRFQ.reference_id)
            .join(User, User.id == VendorRFQ.updated_by)
            .outerjoin(Vendor, Vendor.id == VendorRFQ.vendor_id)
            .filter(VendorRFQ.is_deleted.is_(False))
            .order_by(VendorRFQ.transaction_date.desc())
        )

        if id_list:
            query = (
                query
                .filter(VendorRFQ.id.in_(id_list))
            )

        if search_query:
            query = (
                query
                .filter(or_(
                    VendorRFQ.id.ilike(f"%{search_query}%"),
                ))
            )

        total = query.count()

        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)

        item_list: List[VendorRFQ] = query.all()
        if not item_list:
            return (
                HTTPStatus.NOT_FOUND,
                "Vendor RFQ tidak ditemukan.",
                [],
                total,
            )
        item_data_list = self.many_schema.dump(item_list)

        return (
            HTTPStatus.OK,
            "Vendor RFQ ditemukan.",
            item_data_list,
            total,
        )
