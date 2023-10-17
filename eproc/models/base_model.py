import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import DateTime
from traceback import format_exc
from typing import List

from eproc import app_logger, db, error_logger
from eproc.helpers.commons import wibnow

session: Session = db.session


class WIBNow(FunctionElement):
    type = DateTime(timezone=True)


@compiles(WIBNow, "postgresql")
def pg_wibnow(element, compiler, **kwargs):
    return "TIMEZONE('Asia/Jakarta', CURRENT_TIMESTAMP)"


class BaseModel(db.Model):
    __abstract__ = True

    created_at = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        server_default=WIBNow(),
        nullable=False,
    )
    updated_by = sa.Column(sa.String(20))
    updated_at = sa.Column(
        sa.DateTime(timezone=True),
        default=wibnow(),
        onupdate=WIBNow(),
        nullable=False,
        server_default=WIBNow(),
        server_onupdate=WIBNow(),
    )
    is_deleted = sa.Column(sa.Boolean(), default=False, server_default="false")
    deleted_at = sa.Column(sa.DateTime(timezone=True))

    def save(self) -> "BaseModel":
        try:
            session.add(self)
            session.commit()
            try:
                app_logger.info(f"Added to { self.__tablename__ } :: ID { self.id }")
            except:
                app_logger.info(f"Added to { self.__tablename__ } :: {self.__dict__}")  # TODO
            return self

        except Exception as e:
            session.rollback()
            try:
                error_logger.error(f"Error while adding to { self.__tablename__ } :: ID { self.id }, error: {e}, {format_exc()}")
            except:
                error_logger.error(f"Error while adding to { self.__tablename__ } :: x, error: {e}, {format_exc()}")  # TODO
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
            self.deleted_at = datetime.WIBNow()

            session.add(self)
            session.commit()
            try:
                app_logger.info(f"Deleted from { self.__tablename__ } :: ID { self.id }")
            except:
                app_logger.info(f"Deleted from { self.__tablename__ } :: {self.__dict__}")  # TODO
            return self

        except Exception as e:
            session.rollback()
            try:
                error_logger.error(f"Error while deleting from { self.__tablename__ } :: ID { self.id }, error: {e}, {format_exc()}")
            except:
                error_logger.error(f"Error while deleting from { self.__tablename__ } :: x, error: {e}, {format_exc()}")  # TODO
            raise
    
    def hard_delete(self) -> "BaseModel":
        try:
            session.delete(self)
            session.commit()
            try:
                app_logger.info(f"Hard-deleted from { self.__tablename__ } :: ID { self.id }")
            except:
                app_logger.info(f"Hard-deleted from { self.__tablename__ } :: {self.__dict__}")  # TODO

        except Exception as e:
            session.rollback()
            try:
                error_logger.error(f"Error while hard-deleting from { self.__tablename__ } :: ID { self.id }, error: {e}, {format_exc()}")
            except:
                error_logger.error(f"Error while hard-deleting from { self.__tablename__ } :: x, error: {e}, {format_exc()}")  # TODO
            raise

    def bulk_delete(self, objects: List[dict]) -> List[dict]:
        id_list = [obj.get("id") for obj in objects]
        try:
            for data in objects:
                data["is_deleted"] = True
                data["deleted_at"] = datetime.WIBNow()
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
            try:
                app_logger.info(f"Updated on { self.__tablename__ } :: ID { self.id }")
            except:
                app_logger.info(f"Updated on { self.__tablename__ } :: {self.__dict__}")  # TODO
            return self

        except Exception as e:
            session.rollback()
            try:
                error_logger.error(f"Error while updating on { self.__tablename__ } :: ID { self.id }, error: {e}, {format_exc()}")
            except:
                error_logger.error(f"Error while updating on { self.__tablename__ } :: x, error: {e}, {format_exc()}")  # TODO
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
