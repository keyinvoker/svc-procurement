from http import HTTPStatus
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from typing import List, Optional, Tuple

from eproc.helpers.commons import get_next_sequence_number
from eproc.helpers.rfq import (
    add_items,
    get_next_document_number,
)
from eproc.models.companies.branches import Branch
from eproc.models.references import Reference
from eproc.models.users.users import User
from eproc.models.vendors.vendors import Vendor
from eproc.models.rfqs.rfqs import RFQ
from eproc.schemas.rfqs import RFQAutoSchema


class RFQController:
    def __init__(self):
        self.schema = RFQAutoSchema()
        self.many_schema = RFQAutoSchema(many=True)
    
    def _stringify_vendor_id_list(
        self, vendor_id_list: List[str]
    ) -> str:

        return (
            str(vendor_id_list)
            .replace("'", "")
            .replace("\"", "")
            .replace("[", "")
            .replace("]", "")
            .replace(", ", ";")
        )

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        Procurer = aliased(User)

        query = (
            RFQ.query
            .with_entities(
                RFQ.id,
                RFQ.vendor_id_list,
                Vendor.name.label("vendor_name"),
                RFQ.branch_id,
                Branch.first_address.label("branch_first_address"),
                Branch.second_address.label("branch_second_address"),
                RFQ.reference_id,
                Reference.description.label("reference_description"),
                RFQ.procured_by.label("procurer_id"),
                Procurer.full_name.label("procurer_full_name"),
                User.full_name.label("updated_by"),
                RFQ.document_number,
                RFQ.transaction_date,
                RFQ.year,
                RFQ.month,
                RFQ.description,
                RFQ.app_source,
                RFQ.sequence_number,
                RFQ.dref1,
                RFQ.dref2,
                RFQ.dref3,
                RFQ.flag1,
                RFQ.flag2,
                RFQ.temps,
            )
            .join(Reference, Reference.id == RFQ.reference_id)
            .join(Procurer, Procurer.id == RFQ.procured_by)
            .join(User, User.id == RFQ.updated_by)
            .outerjoin(Branch, Branch.id == RFQ.branch_id)
            .filter(RFQ.is_deleted.is_(False))
            .order_by(RFQ.transaction_date.desc())
        )

        if id_list:
            query = (
                query
                .filter(RFQ.id.in_(id_list))
            )

        if search_query:
            query = (
                query
                .filter(or_(
                    RFQ.id.ilike(f"%{search_query}%"),
                ))
            )

        total = query.count()

        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)

        item_list: List[RFQ] = query.all()
        if not item_list:
            return (
                HTTPStatus.NOT_FOUND,
                "RFQ tidak ditemukan.",
                [],
                total,
            )
        item_data_list = self.many_schema.dump(item_list)

        return (
            HTTPStatus.OK,
            "RFQ ditemukan.",
            item_data_list,
            total,
        )
    
    def create(self, **kwargs) -> Tuple[HTTPStatus, str]:

        branch_id = kwargs.get("branch_id")
        procured_by = kwargs.get("procured_by")
        year = kwargs.get("year")
        month = kwargs.get("month")
        purchase_request_id_list = kwargs.get("purchase_request_id_list")
        vendor_id_list = kwargs.get("vendor_id_list")
        description = kwargs.get("description")
        transaction_type = kwargs.get("transaction_type")

        existing_entry: RFQ = (
            RFQ.query
            .filter(
                RFQ.branch_id == branch_id,
                RFQ.procured_by == procured_by,
                RFQ.year == year,
                RFQ.month == month,
                RFQ.description == description,
                RFQ.transaction_type == transaction_type,
            )
            .first()
        )
        if existing_entry:
            return (
                HTTPStatus.CONFLICT,
                f"Sudah ada PR dengan id: {existing_entry.id}",
            )

        next_sequence_number = get_next_sequence_number(
            RFQ, year, month
        )

        next_document_number = get_next_document_number(
            year, month, next_sequence_number
        )

        vendor_id_list_string = (
            self._stringify_vendor_id_list(vendor_id_list)
        )

        rfq: RFQ = (
            RFQ(
                branch_id=branch_id,
                procured_by=procured_by,
                updated_by=procured_by,
                vendor_id_list=vendor_id_list_string,
                year=year,
                month=month,
                description=description,
                sequence_number=next_sequence_number,
                transaction_type=transaction_type,
                document_number=next_document_number,
                reference_id=0,
            )
        )

        rfq.save()

        message = f"Berhasil menambahkan RFQ baru dengan id: {rfq.id}"

        failed_item_ids = add_items(
            rfq_id=rfq.id,
            purchase_request_id_list=purchase_request_id_list
        )
        if failed_item_ids:
            message += f", gagal menambahkan barang dari PR dengan id: {failed_item_ids}"
        else:
            message += " dan semua barang."

        return HTTPStatus.CREATED, message
