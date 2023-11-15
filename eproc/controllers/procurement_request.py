from datetime import datetime
from http import HTTPStatus
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from traceback import format_exc
from typing import List, Optional, Tuple

from eproc import error_logger
from eproc.helpers.commons import get_next_sequence_number
from eproc.models.assessments.procurement_request_assessments import (
    ProcurementRequestAssessment
)
from eproc.models.companies.branches import Branch
from eproc.models.companies.directorates import Directorate
from eproc.models.companies.divisions import Division
from eproc.models.companies.departments import Department
from eproc.models.cost_centers import CostCenter
from eproc.models.items.item_classes import ItemClass
from eproc.models.items.item_categories import ItemCategory
from eproc.models.items.procurement_request_items import ProcurementRequestItem
from eproc.models.procurement_requests import ProcurementRequest
from eproc.models.references import Reference
from eproc.models.users.employees import Employee
from eproc.models.users.users import User
from eproc.schemas.items.procurement_request_items import (
    ProcurementRequestItemAutoSchema
)
from eproc.schemas.procurement_requests import (
    ProcurementRequestAutoSchema,
    ProcurementRequestDetailSchema,
)


class ProcurementRequestController:
    def __init__(self):
        self.schema = ProcurementRequestAutoSchema()
        self.many_schema = ProcurementRequestAutoSchema(many=True)
        self.detail_schema = ProcurementRequestDetailSchema()

    def get_detail(self, id: int) -> Tuple[HTTPStatus, str, Optional[dict]]:
        try:

            assessment_notes = func.array_agg(
                ProcurementRequestAssessment.assessment_notes
            ).label("assessment_notes")

            Assessor = aliased(User)
            assessors = func.array_agg(Assessor.full_name).label("assessors")

            result = (
                ProcurementRequest.query
                .with_entities(
                    ProcurementRequest.id,
                    ProcurementRequest.document_number,
                    ProcurementRequest.year,
                    ProcurementRequest.month,
                    ProcurementRequest.description,
                    ProcurementRequest.transaction_date,

                    ProcurementRequest.item_class_id,
                    ItemClass.description.label("item_class_name"),

                    ProcurementRequest.item_category_id,
                    ItemCategory.description.label("item_group_name"),

                    ProcurementRequest.branch_id,
                    Branch.description.label("branch_name"),
                    ProcurementRequest.directorate_id,
                    Directorate.description.label("directorate_name"),
                    ProcurementRequest.division_id,
                    Division.description.label("division_name"),
                    ProcurementRequest.department_id,
                    Department.description.label("department_name"),

                    ProcurementRequest.reference_id,
                    Reference.description.label("reference_description"),

                    ProcurementRequest.preparer_id,
                    User.full_name.label("preparer_full_name"),

                    ProcurementRequest.requester_id,
                    Employee.full_name.label("requester_full_name"),

                    ProcurementRequest.cost_center_id,
                    CostCenter.description.label("cost_center_description"),

                    assessment_notes,
                    assessors,
                )
                .join(ItemClass, ItemClass.id == ProcurementRequest.item_class_id)
                .join(ItemCategory, ItemCategory.id == ProcurementRequest.item_category_id)
                .join(Branch, Branch.id == ProcurementRequest.branch_id)
                .join(Directorate, Directorate.id == ProcurementRequest.directorate_id)
                .join(Division, Division.id == ProcurementRequest.division_id)
                .join(Department, Department.id == ProcurementRequest.department_id)
                .join(Reference, Reference.id == ProcurementRequest.reference_id)
                .join(User, User.id == ProcurementRequest.preparer_id)
                .join(Employee, Employee.id == ProcurementRequest.requester_id)
                .join(CostCenter, CostCenter.id == ProcurementRequest.cost_center_id)
                .join(
                    ProcurementRequestAssessment,
                    ProcurementRequestAssessment.procurement_request_id == ProcurementRequest.id
                )
                .join(Assessor, Assessor.id == ProcurementRequestAssessment.assessor_user_id)
                .filter(ProcurementRequest.id == id)
                .filter(ProcurementRequest.is_deleted.is_(False))
                .group_by(
                    ProcurementRequest.id,
                    ItemClass.id,
                    ItemCategory.id,
                    Branch.id,
                    Directorate.id,
                    Division.id,
                    Department.id,
                    Reference.description,
                    User.id,
                    Employee.id,
                    CostCenter.id,
                    # ProcurementRequestAssessment.created_at,
                )
                .order_by(
                    ProcurementRequest.id,
                    # ProcurementRequestAssessment.created_at.desc()
                )
                .first()
            )

            if not result:
                return (
                    HTTPStatus.NOT_FOUND,
                    "Data detail PR tidak ditemukan.",
                    data
                )

            data = self.detail_schema.dump(result)
            return (
                HTTPStatus.OK,
                "Data detail PR ditemukan.",
                data
            )

        except Exception as e:
            error_logger.error(f"Error on PRController:get_detail :: {e}, {format_exc()}")
            return (
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "Terjadi kesalahan saat mengambil data detail PR.",
                None
            )

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            ProcurementRequest.query
            .with_entities(
                ProcurementRequest.id,
                ProcurementRequest.document_number,

                ProcurementRequest.branch_id,
                Branch.description.label("branch_name"),
                ProcurementRequest.directorate_id,
                Directorate.description.label("directorate_name"),
                ProcurementRequest.division_id,
                Division.description.label("division_name"),
                ProcurementRequest.department_id,
                Department.description.label("department_name"),

                ProcurementRequest.reference_id,
                Reference.description.label("reference_description"),

                ProcurementRequest.requester_id,
                Employee.full_name.label("requester_full_name"),
            )
            .filter(ProcurementRequest.is_deleted.is_(False))
            .join(Branch, Branch.id == ProcurementRequest.branch_id)
            .join(Directorate, Directorate.id == ProcurementRequest.directorate_id)
            .join(Division, Division.id == ProcurementRequest.division_id)
            .join(Department, Department.id == ProcurementRequest.department_id)
            .join(Reference, Reference.id == ProcurementRequest.reference_id)
            .join(Employee, Employee.id == ProcurementRequest.requester_id)
            .order_by(ProcurementRequest.transaction_date.desc())
        )

        if id_list:
            query = (
                query
                .filter(ProcurementRequest.id.in_(id_list))
            )

        if search_query:
            query = (
                query
                .filter(or_(
                    ProcurementRequest.id.ilike(f"%{search_query}%"),
                ))
            )

        total = query.count()

        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)

        item_list: List[ProcurementRequest] = query.all()
        if not item_list:
            return (
                HTTPStatus.NOT_FOUND,
                "Procurement Request tidak ditemukan.",
                [],
                total,
            )
        item_data_list = self.many_schema.dump(item_list)

        return (
            HTTPStatus.OK,
            "Procurement Request ditemukan.",
            item_data_list,
            total,
        )
    
    def get_items(
        self, procurement_request_id: int
    ) -> Tuple[HTTPStatus, str, Optional[List[dict]], int]:

        query = (
            ProcurementRequestItem.query
            .filter(ProcurementRequestItem.procurement_request_id == procurement_request_id)
            .filter(ProcurementRequestItem.is_deleted.is_(False))
            .order_by(ProcurementRequestItem.lnnum)
        )

        total = query.count()
        if total == 0:
            return (
                HTTPStatus.NOT_FOUND,
                f"Tidak ditemukan barang dari PR dengan id: {procurement_request_id}.",
                None,
                0
            )

        results = query.all()
        data = ProcurementRequestItemAutoSchema(many=True).dump(results)

        return (
            HTTPStatus.OK,
            f"Ditemukan barang dari PR dengan id: {procurement_request_id}.",
            data,
            total
        )
    
    def create(self, **kwargs) -> Tuple[HTTPStatus, str, Optional[dict]]:

        message = "Berhasil menambahkan PR"
        data = None

        branch_id = kwargs.get("branch_id")
        directorate_id = kwargs.get("directorate_id")
        division_id = kwargs.get("division_id")
        department_id = kwargs.get("department_id")
        preparer_id = kwargs.get("preparer_id")
        requester_id = kwargs.get("requester_id")
        year = kwargs.get("year")
        month = kwargs.get("month")
        description = kwargs.get("description")
        item_class_id = kwargs.get("item_class_id")
        item_category_id = kwargs.get("item_category_id")
        item_list: List[dict] = kwargs.get("item_list")

        cost_center_id = ItemCategory.query.with_entities(ItemCategory.cost_center_id).filter(ItemCategory.id == item_category_id).first().cost_center_id

        next_sequence_number = get_next_sequence_number(
            ProcurementRequest, year, month
        )

        procurement_request: ProcurementRequest = (
            ProcurementRequest(
                branch_id=branch_id,
                directorate_id=directorate_id,
                division_id=division_id,
                department_id=department_id,
                cost_center_id=cost_center_id,
                preparer_id=preparer_id,
                requester_id=requester_id,
                updated_by=preparer_id,
                year=year,
                month=month,
                description=description,
                item_class_id=item_class_id,
                item_category_id=item_category_id,
                sequence_number=next_sequence_number,
                transaction_type="REG",
            )
        )

        procurement_request.save()
        print(f"procurement_request.id = {procurement_request.id}")

        failed_item_ids: List[Optional[str]] = list()
        failed_item_data: List[Optional[dict]] = list()
        for index, item in enumerate(item_list):
            try:
                item_id = item.get("id")
                unit_of_measurement = item.get("unit_of_measurement")
                quantity = item.get("quantity")
                required_date = item.get("required_date")
                notes = item.get("notes")

                ProcurementRequestItem(
                    procurement_request_id=procurement_request.id,
                    item_id=item_id,
                    lnnum=(index + 1),
                    unit_of_measurement=unit_of_measurement,
                    quantity=quantity,
                    required_date=required_date,
                    required_days_interval=datetime.fromisoformat(required_date).replace(tzinfo=None),
                    notes=notes,
                    currency_id="IDR",
                    aprqt=0,  # TODO: field gak guna
                ).save()

            except Exception as e:
                error_logger.error(f"Failed to add PR Item :: {e}, data: {item}")

                failed_item_ids.append(item_id)
                failed_item_data.append(item)
                continue
        
        if failed_item_ids:
            message += f", gagal menambahkan barang dengan ID: {failed_item_ids}"
            data = dict(failed_item_data=failed_item_data)
        else:
            message += " dan semua barang."

        return HTTPStatus.OK, message, data
