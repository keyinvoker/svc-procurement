from http import HTTPStatus
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from typing import List, Optional, Tuple

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
                RFQ.vendor_id,
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
            .outerjoin(Vendor, Vendor.id == RFQ.vendor_id)
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
    
    def create(self, **kwargs) -> Tuple[HTTPStatus, str, Optional[dict]]:

        branch_id = kwargs.get("branch_id")
        procured_by = kwargs.get("procured_by")
        year = kwargs.get("year")
        month = kwargs.get("month")
        description = kwargs.get("description")
        transaction_type = kwargs.get("transaction_type")
        item_list: List[dict] = kwargs.get("item_list")

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
        )
        if existing_entry:
            return (
                HTTPStatus.CONFLICT,
                f"Sudah ada PR dengan id: {existing_entry.id}",
                None
            )

        # cost_center_id = (
        #     ItemCategory.query
        #     .with_entities(ItemCategory.cost_center_id)
        #     .filter(ItemCategory.id == item_category_id)
        #     .first()
        #     .cost_center_id
        # )

        next_sequence_number = get_next_sequence_number(
            ProcurementRequest, year, month
        )

        next_document_number = get_next_document_number(
            transaction_type, year, month, next_sequence_number
        )

        procurement_request: RFQ = (
            RFQ(
                branch_id=branch_id,
                procured_by=procured_by,
                requester_id=requester_id,
                updated_by=preparer_id,
                year=year,
                month=month,
                description=description,
                item_class_id=item_class_id,
                item_category_id=item_category_id,
                sequence_number=next_sequence_number,
                transaction_type=transaction_type,
                document_number=next_document_number,
            )
        )

        procurement_request.save()

        message = f"Berhasil menambahkan PR baru dengan id: {procurement_request.id}"
        data = None

        failed_item_ids, failed_item_data = add_items(
            procurement_request_id=procurement_request.id,
            item_list=item_list,
        )
        if failed_item_ids:
            message += f", gagal menambahkan barang dengan id: {failed_item_ids}"
            data = dict(failed_item_data=failed_item_data)
        else:
            message += " dan semua barang."

        return HTTPStatus.OK, message, data
