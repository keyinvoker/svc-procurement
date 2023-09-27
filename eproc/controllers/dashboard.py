from eproc.models.rfqs import RFQ
from eproc.models.vendors.vendors import Vendor
from eproc.models.vendor_rfqs import VendorRFQ


class DashboardController:
    def get_active_vendor_count(self):
        return (
            Vendor.query
            .filter(Vendor.is_active.is_(True))
            .filter(Vendor.is_deleted.is_(False))
            .count()
        )
    
    def get_pending_vendor_count(self):
        return (
            Vendor.query
            .filter(Vendor.is_active.is_(False))
            .filter(Vendor.is_deleted.is_(False))
            .count()
        )

    def get_pending_rfq_count(self):
        return (
            RFQ.query
            .filter(RFQ.reference_id != 56)
            .filter(RFQ.is_deleted.is_(False))
            .count()
        )

    def get_pending_vendor_price_count(self):
        return (
            VendorRFQ.query
            .filter(VendorRFQ.reference_id != 56)
            .filter(VendorRFQ.is_deleted.is_(False))
            .count()
        )
