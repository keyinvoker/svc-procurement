from http import HTTPStatus
from typing import List, Optional, Tuple

from eproc.helpers.commons import get_next_sequence_number
from eproc.models.cost_centers import CostCenter
from eproc.models.invoices import Invoice
from eproc.models.references import Reference
from eproc.models.cost_centers import CostCenter
from eproc.models.vendors.vendors import Vendor
from eproc.models.purchase_orders.purchase_orders import PurchaseOrder
from eproc.models.references import Reference
from eproc.schemas.invoices import (
    InvoiceSchema,
    InvoiceDetailSchema,
)


class InvoiceController:
    def __init__(self):
        self.schema = InvoiceSchema()
        self.many_schema = InvoiceSchema(many=True)
        self.detail_schema = InvoiceDetailSchema()
    
    def get_detail(self, id: int) -> Tuple[HTTPStatus, str, Optional[dict]]:
        invoice: Invoice = (
            Invoice.query
            .with_entities(
                Invoice.id,
                Invoice.purchase_order_id,
                PurchaseOrder.document_number.label("purchase_order_document_number"),
                PurchaseOrder.vendor_id.label("purchase_order_vendor_id"),
                Vendor.name.label("purchase_order_vendor_name"),
                Invoice.vendor_id,
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
                Invoice.document_number,
                Invoice.description,
                # Invoice.image_path,
                Invoice.tax_percentage,
            )
            .join(PurchaseOrder, PurchaseOrder.id == Invoice.purchase_order_id)
            .join(Vendor, Vendor.id == PurchaseOrder.vendor_id)
            .join(CostCenter, CostCenter.id == Invoice.cost_center_id)
            .join(Reference, Reference.id == Invoice.reference_id)
            .filter(
                Invoice.id == id,
                Invoice.is_deleted.is_(False),
            )
            .first()
        )
        if not invoice:
            return (
                HTTPStatus.NOT_FOUND,
                f"Tidak ditemukan invoice dengan id: {id}",
                None
            )

        invoice_data = self.detail_schema.dump(invoice)

        return (
            HTTPStatus.OK,
            "Invoice ditemukan.",
            invoice_data,
        )
    
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

    def update(self, **kwargs) -> Tuple[HTTPStatus, str, Optional[dict]]:
        id = kwargs.get("id")
        invoice_date = kwargs.get("invoice_date")
        invoice_number = kwargs.get("invoice_number")
        invoice_amount = kwargs.get("invoice_amount")
        invoice_image = kwargs.get("invoice_image")
        description = kwargs.get("description")
        updated_by = kwargs.get("updated_by")

        if (
            not invoice_date
            and not invoice_number
            and not invoice_amount
            and not invoice_image
            and not description
        ):
            return (
                HTTPStatus.BAD_REQUEST,
                "Tidak ada data yang dimasukkan.",
                None,
            )

        invoice: Invoice = (
            Invoice.query
            .filter(
                Invoice.id == id,
                Invoice.is_deleted.is_(False)
            )
            .first()
        )
        if not invoice:
            return (
                HTTPStatus.NOT_FOUND,
                f"Invoice dengan id {id} tidak ditemukan.",
                None
            )

        image_path = None
        if invoice_image:
            image_path = f"/path/to/{invoice_image}"
            invoice.image_path = image_path

        if (
            (not invoice_date or invoice_date == str(invoice.invoice_date))
            and (not invoice_number or invoice_number == invoice.invoice_number)
            and (not invoice_amount or invoice_amount == invoice.invoice_amount)
            and (not image_path or image_path == invoice.image_path)
            and (not description or description == invoice.description)
        ):
            return (
                HTTPStatus.OK,
                "Invoice tidak perlu diperbarui.",
                None,
            )

        if invoice_date:
            invoice.invoice_date = invoice_date
        if invoice_number:
            invoice.invoice_number = invoice_number
        if invoice_amount:
            invoice.invoice_amount = invoice_amount
        if description:
            invoice.description = description

        invoice.updated_by = updated_by
        invoice.update()

        return (
            HTTPStatus.OK,
            "Invoice berhasil diperbarui.",
            self.schema.dump(invoice)
        )