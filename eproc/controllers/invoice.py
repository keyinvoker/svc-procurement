from http import HTTPStatus
from typing import List, Optional, Tuple

from eproc.helpers.commons import get_next_sequence_number
from eproc.models.cost_centers import CostCenter
from eproc.models.invoices import Invoice
from eproc.models.references import Reference
from eproc.models.vendors.vendors import Vendor
from eproc.schemas.invoices import InvoiceSchema


class InvoiceController:
    def __init__(self):
        self.schema = InvoiceSchema()
        self.many_schema = InvoiceSchema(many=True)
    
    def get_list(
        self,
        **kwargs
    ) -> Tuple[HTTPStatus, str, List[Optional[dict]], int]:

        id_list: List[str] = kwargs.get("id_list")
        limit: Optional[int] = kwargs.get("limit")
        offset: int = kwargs.get("offset")

        query = (
            Invoice.query
            .with_entities(
                Invoice.id,
                Invoice.vendor_id,
                Vendor.name.label("vendor_name"),
                Invoice.cost_center_id,
                CostCenter.description.label("cost_center_description"),
                Invoice.reference_id,
                Reference.description.label("reference_description"),
                Invoice.transaction_date,
                Invoice.year,
                Invoice.month,
                Invoice.invoice_date,
                Invoice.invoice_number,
                Invoice.invoice_amount,
                Invoice.termin,
                Invoice.purchase_order_id,
                Invoice.document_number,
                Invoice.description,
                Invoice.tax_percentage,
            )
            .join(Vendor, Vendor.id == Invoice.vendor_id)
            .join(CostCenter, CostCenter.id == Invoice.cost_center_id)
            .join(Reference, Reference.id == Invoice.reference_id)
            .filter(Invoice.is_deleted.is_(False))
            .order_by(Invoice.id)
        )

        if id_list:
            query = (
                query
                .filter(Invoice.id.in_(id_list))
            )

        total = query.count()

        if limit:
            query = query.limit(limit)

        if offset > 0:
            query = query.offset(offset)

        results: List[Invoice] = query.all()
        if not results:
            return (
                HTTPStatus.NOT_FOUND,
                "Invoice tidak ditemukan.",
                [],
                total,
            )
        data_list = self.many_schema.dump(results)

        return (
            HTTPStatus.OK,
            "Invoice ditemukan.",
            data_list,
            total,
        )

    def create(self, **kwargs) -> Tuple[HTTPStatus, str, dict]:
        purchase_order_id = kwargs.get("purchase_order_id")
        year = kwargs.get("year")
        month = kwargs.get("month")
        termin = kwargs.get("termin")
        invoice_number = kwargs.get("invoice_number")
        invoice_date = kwargs.get("invoice_date")
        invoice_amount = kwargs.get("invoice_amount")
        image_path = kwargs.get("image_path")
        description = kwargs.get("description")
        updated_by = kwargs.get("updated_by")

        sequence_number = get_next_sequence_number(
            Invoice, year, month
        )

        invoice: Invoice = Invoice(
            purchase_order_id=purchase_order_id,
            year=year,
            month=month,
            termin=termin,
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            invoice_amount=invoice_amount,
            image_path=image_path,
            description=description,
            sequence_number=sequence_number,
            updated_by=updated_by,
        )

        invoice.save()

        return (
            HTTPStatus.CREATED,
            "Invoice baru berhasil ditambahkan.",
            self.schema.dump(invoice)
        )
