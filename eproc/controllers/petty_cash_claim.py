from http import HTTPStatus
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from typing import List, Optional, Tuple

from eproc.models.companies.branches import Branch
from eproc.models.cost_centers import CostCenter
from eproc.models.petty_cash_claims import PettyCashClaim
from eproc.models.references import Reference
from eproc.models.users.employees import Employee
from eproc.models.users.users import User
from eproc.schemas.petty_cash_claims import PettyCashClaimSchema


class PettyCashClaimController:
    def __init__(self, **kwargs):
        self.schema = PettyCashClaimSchema()
        self.many_schema = PettyCashClaimSchema(many=True)
    
    def get_list(
        self, **kwargs
    ) -> Tuple[HTTPStatus, str, Optional[dict]]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        Preparer = aliased(User)

        query = (
            PettyCashClaim.query
            .with_entities(
                PettyCashClaim.id,
                PettyCashClaim.document_number,
                PettyCashClaim.description,
                PettyCashClaim.branch_id,
                Branch.description.label("branch_name"),
                PettyCashClaim.reference_id,
                Reference.description.label("reference_description"),
                PettyCashClaim.preparer_id,
                User.full_name.label("preparer_full_name"),
                PettyCashClaim.requester_id,
                Employee.full_name.label("requester_full_name"),
                PettyCashClaim.cost_center_id,
                CostCenter.description.label("cost_center_description"),
                User.full_name.label("updated_by"),
            )
            .filter(PettyCashClaim.is_deleted.is_(False))
            .outerjoin(Branch, Branch.id == PettyCashClaim.branch_id)
            .outerjoin(CostCenter, CostCenter.id == PettyCashClaim.cost_center_id)
            .outerjoin(Reference, Reference.id == PettyCashClaim.reference_id)
            .outerjoin(Employee, Employee.id == PettyCashClaim.requester_id)
            .outerjoin(User, User.id == PettyCashClaim.updated_by)
            .outerjoin(Preparer, Preparer.id == PettyCashClaim.preparer_id)
            .order_by(PettyCashClaim.transaction_date.desc())
        )

        if id_list:
            query = (
                query
                .filter(PettyCashClaim.id.in_(id_list))
            )

        if search_query:
            query = (
                query
                .filter(or_(
                    PettyCashClaim.id.ilike(f"%{search_query}%"),
                ))
            )

        total = query.count()

        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)

        results: List[PettyCashClaim] = query.all()
        if not results:
            return (
                HTTPStatus.NOT_FOUND,
                "Petty Cash tidak ditemukan.",
                [],
                total,
            )
        data_list = self.many_schema.dump(results)

        return (
            HTTPStatus.OK,
            "Petty Cash ditemukan.",
            data_list,
            total,
        )
