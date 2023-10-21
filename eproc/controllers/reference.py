from http import HTTPStatus
from typing import Optional, Tuple
from traceback import format_exc

from eproc import error_logger
from eproc.models.enums import SystemConfigOption as Option
from eproc.models.references import Reference
from eproc.schemas.references import ReferenceAutoSchema


class ReferenceController:
    def __init__(self, **kwargs):
        self.schema = ReferenceAutoSchema()
        self.many_schema = ReferenceAutoSchema(many=True)
    
    def get_system_configuration(
        self,
        option: str
    ) -> Tuple[HTTPStatus, str, Optional[dict]]:
        
        http_status = HTTPStatus.OK
        message = ""
        data = None

        try:
            keyword = Option[option].value
            results = (
                Reference.query
                .filter(
                    Reference.description.ilike(f"%{keyword}%"),
                    Reference.is_active.is_(True),
                    Reference.is_deleted.is_(False),
                )
                .order_by(Reference.id)
                .all()
            )

            if not results:
                http_status = HTTPStatus.NOT_FOUND
                message = f"Tidak ditemukan konfigurasi sistem untuk opsi: {option}"
            else:
                message = f"Konfigurasi sistem ditemukan untuk opsi: {option}"
                data = self.many_schema.dump(results)

        except Exception as e:
            error_logger.error(f"Error on ReferenceController:get_system_configuration :: {e}, {format_exc()}")

            http_status = HTTPStatus.INTERNAL_SERVER_ERROR
            message = f"Terjadi kesalahan saat mengambil konfigurasi sistem untuk opsi: {option}"

        return http_status, message, data
