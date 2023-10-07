from http import HTTPStatus
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from typing import List, Optional, Tuple

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
        FirstApprover = aliased(Employee)
        SecondApprover = aliased(Employee)
        # ThirdApprover = aliased(Employee)

        from eproc import app_logger
        app_logger.info(f"Employee:get_detail :: id: {id}")

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
                # ThirdApprover.id.label("third_approver_id"),
                # ThirdApprover.full_name.label("third_approver_full_name"),
                # ThirdApprover.is_active.label("third_approver_is_active"),
                Employee.is_active,
                Employee.updated_at,
                Employee.updated_by,
            )
            .join(FirstApprover, FirstApprover.id == Employee.first_approver_id)
            # .join(SecondApprover, SecondApprover.id == Employee.second_approver_id)  # TODO: FIX - if second_approver is null, then 404
            # .join(ThirdApprover, ThirdApprover.id == Employee.third_approver_id)
            .join(Branch, Branch.id == Employee.branch_id)
            .join(Directorate, Directorate.id == Employee.directorate_id)
            .join(Division, Division.id == Employee.division_id)
            .join(Department, Department.id == Employee.department_id)
            .filter(Employee.id == id)
            .filter(Employee.is_deleted.is_(False))
            .first()
        )
        
        if not employee:
            return (
                HTTPStatus.NOT_FOUND,
                "Employee tidak ditemukan.",
                None
            )
        print(f"directorate_name :: {employee.directorate_name}")

        employee_data = self.detail_schema.dump(employee)

        return HTTPStatus.OK, "Employee ditemukan.", employee_data

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        entity_id: str = kwargs.get("entity_id")
        search_query: str = kwargs.get("search_query").strip()
        limit: int = kwargs.get("limit")
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
                "Employee tidak ditemukan.",
                [],
                total
            )
        employee_data_list = self.many_schema.dump(employee_list)

        return (
            HTTPStatus.OK,
            "Employee ditemukan.",
            employee_data_list,
            total
        )
