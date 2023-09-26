from http import HTTPStatus
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from typing import List, Optional, Tuple

from eproc.models.references import Reference
from eproc.models.users.users import User
from eproc.schemas.users.users import UserAutoSchema


class UserController:
    def __init__(self):
        self.schema = UserAutoSchema()
        self.many_schema = UserAutoSchema(many=True)
    
    def get_detail(self, id: str) -> Tuple[HTTPStatus, str, Optional[dict]]:
        user: User = (
            User.query
            .filter(User.id == id)
            .filter(User.is_deleted.is_(False))
            .first()
        )
        
        if not user:
            return (
                HTTPStatus.NOT_FOUND,
                "User tidak ditemukan.",
                None
            )

        user_data = self.schema.dump(user)

        return HTTPStatus.OK, "User ditemukan.", user_data

    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        search_query: str = kwargs.get("search_query").strip()
        limit: int = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        FirstApprover = aliased(User)

        user_query = (
            User.query
            .with_entities(
                User.id,
                User.full_name,
                User.password,
                User.password_length,
                User.email,
                FirstApprover.full_name.label("first_approve_full_name"),
                User.is_active,
                User.is_locked,
                User.is_anonymous,
                User.is_admin,
                User.updated_at,
                User.updated_by,
                Reference.description.label("status"),
            )
            .join(FirstApprover, FirstApprover.id == User.first_approver_id)
            .join(Reference, Reference.id == User.reference_id)
            .filter(User.is_deleted.is_(False))
        )

        if id_list:
            user_query = user_query.filter(User.id.in_(id_list))
        
        if search_query:
            user_query = (
                user_query
                .filter(or_(
                    User.id.ilike(f"%{search_query}%"),
                    User.full_name.ilike(f"%{search_query}%"),
                ))
            )
        
        total = user_query.count()
        
        if limit:
            user_query = user_query.limit(limit)

        if offset > 0:
            user_query = user_query.offset(offset)
        
        user_list: List[User] = user_query.all()

        if not user_list:
            return (
                HTTPStatus.NOT_FOUND,
                "User tidak ditemukan.",
                [],
                total
            )
        user_data_list = self.many_schema.dump(user_list)

        return (
            HTTPStatus.OK,
            "User ditemukan.",
            user_data_list,
            total
        )
