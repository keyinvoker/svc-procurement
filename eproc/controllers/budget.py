import pandas as pd
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
        )

        if cost_center_id:
            query = query.filter(Budget.cost_center_id == cost_center_id)

        if year:
            query = query.filter(Budget.year == year)

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

        data_list = self.many_schema.dump(result_list)

        return (
            HTTPStatus.OK,
            "Budget ditemukan.",
            data_list,
            total,
        )

    def file_upload(self, user_id: str, df: pd.DataFrame) -> Tuple[HTTPStatus, str]:
        try:

            for _, row in df.iterrows():
                cost_center_id = row["cost center"]
                year = row["year"]
                amount = row["amount"]

                budget: Budget = (
                    Budget.query
                    .filter(
                        Budget.cost_center_id == cost_center_id,
                        Budget.year == year,
                        Budget.is_deleted.is_(False),
                    )
                    .first()
                )

                if budget:
                    if budget.amount != amount:
                        budget.amount = amount
                        budget.upload_count += 1
                        budget.updated_by = user_id
                        budget.update()
                else:
                    Budget(
                        cost_center_id=cost_center_id,
                        year=year,
                        amount=amount,
                        upload_count=1,
                        updated_by=user_id,
                    ).save()

            return (
                HTTPStatus.OK,
                "File terupload dengan sukses."
            )
        except Exception as e:
            error_logger.error(f"Error on BudgetController:file_upload() :: df: {df}, error: {e}, {format_exc()}")
            return (
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "Terjadi kegagalan saat mengupload file."
            )
