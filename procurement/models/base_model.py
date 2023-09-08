import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import DateTime
from traceback import format_exc
from typing import List

from procurement import app_logger, db, error_logger

session: Session = db.session


class utcnow(FunctionElement):
    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kwargs):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class BaseModel(db.Model):
    id = sa.Column(
        sa.BigInteger(),
        primary_key=True,
        autoincrement=True,
    )
    created_at = sa.Column(
        sa.DateTime(),
        default=datetime.utcnow,
        server_default=utcnow(),
    )
    updated_at = sa.Column(
        sa.DateTime(),
        default=datetime.utcnow,
        onupdate=utcnow(),
        server_default=utcnow(),
        server_onupdate=utcnow(),
    )
    is_deleted = sa.Column(
        sa.Boolean(),
        default=False,
        server_default="false",
    )
    deleted_at = sa.Column(sa.DateTime(), default=None)

    def save(self) -> "BaseModel":
        try:
            session.add(self)
            session.commit()
            app_logger.info(f"Added to { self.__tablename__ } :: ID { self.id }")
            return self

        except Exception as e:
            session.rollback()
            error_logger.error(f"Error while adding to { self.__tablename__ } :: ID { self.id }, error: {e}, {format_exc()}")
            raise

    def bulk_save(self, objects: List[dict]) -> List[dict]:
        id_list = [obj.get("id") for obj in objects]
        try:
            session.bulk_save_objects(objects)
            session.commit()
            app_logger.info(f"Bulk-saved on { self.__tablename__ } :: IDs: { id_list }")
            return objects

        except Exception as e:
            session.rollback()
            error_logger.error(f"Error while bulk-saving on { self.__tablename__ } :: IDs: { id_list }, error: {e}, {format_exc()}")
            raise

    def delete(self) -> "BaseModel":
        try:
            self.is_deleted = True
            self.deleted_at = datetime.utcnow()

            session.add(self)
            session.commit()
            app_logger.info(f"Deleted from { self.__tablename__ } :: ID { self.id }")
            return self

        except Exception as e:
            session.rollback()
            error_logger.error(f"Error while deleting from { self.__tablename__ } :: ID { self.id }, error: {e}, {format_exc()}")
            raise
    
    def hard_delete(self) -> "BaseModel":
        try:
            session.delete(self)
            session.commit()
            app_logger.info(f"Hard-deleted from { self.__tablename__ } :: ID { self.id }")

        except Exception as e:
            session.rollback()
            error_logger.error(f"Error while hard-deleting from { self.__tablename__ } :: ID { self.id }, error: {e}, {format_exc()}")
            raise

    def bulk_delete(self, objects: List[dict]) -> List[dict]:
        id_list = [obj.get("id") for obj in objects]
        try:
            for data in objects:
                data["is_deleted"] = True
                data["deleted_at"] = datetime.utcnow()
                session.add(data)

            session.commit()
            app_logger.info(f"Bulk-deleted from { self.__tablename__ } :: IDs: { id_list }")
            return self

        except Exception as e:
            session.rollback()
            error_logger.error(f"Error while bulk-deleting from { self.__tablename__ } :: IDs: { id_list }, error: {e}, {format_exc()}")
            raise

    def update(self, **kwargs) -> "BaseModel":
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        try:
            session.add(self)
            session.commit()
            app_logger.info(f"Updated on { self.__tablename__ } :: ID { self.id }")
            return self

        except Exception as e:
            session.rollback()
            error_logger.error(f"Error while updating on { self.__tablename__ } :: ID { self.id }, error: {e}, {format_exc()}")
            raise

    def bulk_update(self, objects: List[dict]) -> List[dict]:
        id_list = [obj.get("id") for obj in objects]
        try:
            session.bulk_update_mappings(self, objects)
            session.commit()
            app_logger.info(f"Bulk-updated on { self.__tablename__ } :: IDs: { id_list }")
            return self, objects

        except Exception as e:
            session.rollback()
            error_logger.error(f"Error while bulk-updating on { self.__tablename__ } :: IDs: { id_list }, error: {e}, {format_exc()}")
            raise
