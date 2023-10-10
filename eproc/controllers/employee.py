from http import HTTPStatus
from sqlalchemy.sql import case, func, or_
from sqlalchemy.orm import aliased
from typing import List, Optional, Tuple
from traceback import format_exc

from eproc import error_logger
from eproc.models.auth.users_roles import UserRole
from eproc.models.companies.branches import Branch
from eproc.models.companies.departments import Department
from eproc.models.companies.directorates import Directorate
from eproc.models.companies.divisions import Division
from eproc.models.users.employees import Employee
from eproc.schemas.users.employees import (
    EmployeeAutoSchema,
    EmployeeDetailSchema,
)


class EmployeeController:
    def __init__(self):
        self.schema = EmployeeAutoSchema()
        self.many_schema = EmployeeAutoSchema(many=True)
        self.detail_schema = EmployeeDetailSchema()
    
    def get_detail(self, id: str) -> Tuple[HTTPStatus, str, Optional[dict]]:
        try:
            FirstApprover = aliased(Employee)
            SecondApprover = aliased(Employee)
            ThirdApprover = aliased(Employee)

            is_registered = (
                case(
                    (func.count(UserRole.role_id) > 0, True),
                    else_=False
                ).label("is_registered")
            )

            employee: Employee = (
                Employee.query
                .with_entities(
                    Employee.id,
                    Employee.full_name,
                    Employee.email,
                    Employee.phone_number,
                    Employee.branch_id,
                    Branch.description.label("branch_name"),
                    Employee.directorate_id,
                    Directorate.description.label("directorate_name"),
                    Employee.division_id,
                    Division.description.label("division_name"),
                    Employee.department_id,
                    Department.description.label("department_name"),
                    FirstApprover.id.label("first_approver_id"),
                    FirstApprover.full_name.label("first_approver_full_name"),
                    FirstApprover.is_active.label("first_approver_is_active"),
                    SecondApprover.id.label("second_approver_id"),
                    SecondApprover.full_name.label("second_approver_full_name"),
                    SecondApprover.is_active.label("second_approver_is_active"),
                    ThirdApprover.id.label("third_approver_id"),
                    ThirdApprover.full_name.label("third_approver_full_name"),
                    ThirdApprover.is_active.label("third_approver_is_active"),
                    Employee.is_active,
                    Employee.updated_at,
                    Employee.updated_by,
                    is_registered,
                )
                .outerjoin(FirstApprover, FirstApprover.id == Employee.first_approver_id)
                .outerjoin(SecondApprover, SecondApprover.id == Employee.second_approver_id)  # TODO: FIX - if second_approver is null, then 404
                .outerjoin(ThirdApprover, ThirdApprover.id == Employee.third_approver_id)
                .join(Branch, Branch.id == Employee.branch_id)
                .join(Directorate, Directorate.id == Employee.directorate_id)
                .join(Division, Division.id == Employee.division_id)
                .join(Department, Department.id == Employee.department_id)
                .outerjoin(UserRole, UserRole.user_id == Employee.id)
                .filter(Employee.id == id)
                .filter(Employee.is_deleted.is_(False))
                .group_by(
                    Employee.id,
                    Branch.description,
                    Directorate.description,
                    Division.description,
                    Department.description,
                    FirstApprover.id,
                    FirstApprover.full_name,
                    FirstApprover.is_active,
                    SecondApprover.id,
                    SecondApprover.full_name,
                    SecondApprover.is_active,
                    ThirdApprover.id,
                    ThirdApprover.full_name,
                    ThirdApprover.is_active,
                )
                .first()
            )
            
            if not employee:
                return (
                    HTTPStatus.NOT_FOUND,
                    "Pegawai tidak ditemukan.",
                    None
                )

            employee_data = self.detail_schema.dump(employee)

            return HTTPStatus.OK, "Pegawai ditemukan.", employee_data
        except Exception as e:
            error_logger.error(f"Error on EmployeeController:get_detail() :: {e}, {format_exc()}")
            return (
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "Terjadi kegagalan saat mengambil data pegawai.",
                None
            )

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        entity_id: str = kwargs.get("entity_id")
        search_query: str = kwargs.get("search_query").strip()
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        FirstApprover = aliased(Employee)

        employee_query = (
            Employee.query
            .with_entities(
                Employee.id,
                Employee.full_name,
                Employee.email,
                FirstApprover.full_name.label("first_approver_full_name"),
                Employee.is_active,
                Employee.updated_at,
                Employee.updated_by,
            )
            .join(FirstApprover, FirstApprover.id == Employee.first_approver_id)
            .filter(Employee.is_deleted.is_(False))
        )

        if id_list:
            employee_query = employee_query.filter(Employee.id.in_(id_list))
        
        if entity_id:
            employee_query = employee_query.filter(Employee.entity_id == entity_id)
        
        if search_query:
            employee_query = (
                employee_query
                .filter(or_(
                    Employee.id.ilike(f"%{search_query}%"),
                    Employee.full_name.ilike(f"%{search_query}%"),
                ))
            )
        
        total = employee_query.count()
        
        if limit:
            employee_query = employee_query.limit(limit)

        if offset > 0:
            employee_query = employee_query.offset(offset)
        
        employee_list: List[Employee] = employee_query.all()

        if not employee_list:
            return (
                HTTPStatus.NOT_FOUND,
                "Pegawai tidak ditemukan.",
                [],
                total
            )
        employee_data_list = self.many_schema.dump(employee_list)

        return (
            HTTPStatus.OK,
            "Pegawai ditemukan.",
            employee_data_list,
            total
        )
