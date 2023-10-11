from http import HTTPStatus
from sqlalchemy import or_
from traceback import format_exc
from typing import List, Optional, Tuple

from eproc import error_logger
from eproc.models.budgets import Budget
from eproc.schemas.budgets import BudgetAutoSchema


class BudgetController:
    def __init__(self):
        self.schema = BudgetAutoSchema()
        self.many_schema = BudgetAutoSchema(many=True)

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        cost_center_id: str = kwargs.get("cost_center_id")
        year: int = kwargs.get("year")
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            Budget.query
            .filter(Budget.is_deleted.is_(False))
            .order_by(Budget.year.desc())
            # .order_by(Budget.updated_at.desc())
        )

        if cost_center_id:
            query = query.filter(Budget.id == cost_center_id)

        if year:
            query = query.filter(Budget.id == year)

        total = query.count()

        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)

        result_list: List[Budget] = query.all()
        if not result_list:
            return (
                HTTPStatus.NOT_FOUND,
                "Budget tidak ditemukan.",
                [],
                total,
            )
        for i in result_list:
            print(i.cost_center_id)
        data_list = self.many_schema.dump(result_list)

        return (
            HTTPStatus.OK,
            "Budget ditemukan.",
            data_list,
            total,
        )
