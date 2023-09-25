from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from eproc.models.vendors.vendors import Vendor


class VendorDetailAutoSchema(SQLAlchemyAutoSchema):
    status_text = fields.String()

    @post_dump
    def parse_data(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = float(value)

        if data.get("status_id"):
            from eproc.models.users.references import Reference
            data["status"] = Reference.query.filter(Reference.cdnum == data["status_id"]).first().description  # TODO improve this using Foreign Key

        from eproc.models.vendors.vendor_assessments import VendorAssessment
        vendor_review = VendorAssessment.query.filter(VendorAssessment.vendor_id == data["id"]).first()
        data["review_notes"] = None
        if vendor_review:
            data["review_notes"] = vendor_review.review_notes

        return data

    class Meta:
        model = Vendor
        load_instance = True
        ordered = True
        unknown = EXCLUDE
        exclude = (
            "office_area_file",
            "warehouse_area_file",
            "manufacture_area_file",
            "others_area_file",
            "npwp_file",
            "jamsostek_file",
            "business_establishment_deed_file",
            "siup_file",
            "nbnib_file",
            "siujk_file",
            "sbujk_file",
            "iup_file",
            "sku_file",
            "skdp_file",
            "situ_file",
            "sppkp_file",
            "skt_file",
            "tdp_file",
            "kadin_file",
            "sknkp_file",
            "other_document_file",
        )


class VendorAutoSchema(VendorDetailAutoSchema):
    class Meta:
        model = Vendor
        load_instance = True
        ordered = True
        unknown = EXCLUDE
        exclude = (
            "office_area_file",
            "warehouse_area_file",
            "manufacture_area_file",
            "others_area_file",
            "npwp_file",
            "jamsostek_file",
            "business_establishment_deed_file",
            "siup_file",
            "nbnib_file",
            "siujk_file",
            "sbujk_file",
            "iup_file",
            "sku_file",
            "skdp_file",
            "situ_file",
            "sppkp_file",
            "skt_file",
            "tdp_file",
            "kadin_file",
            "sknkp_file",
            "other_document_file",
        )


class VendorGetInputSchema(Schema):
    id_list = fields.List(
        fields.Integer(),
        dump_default=[],
        load_default=[],
    )
    search_query = fields.String(
        allow_none=True,
        dump_default="",
        load_default="",
    )
    limit = fields.Integer(
        allow_none=True,
        dump_default=None,
        load_default=None,
    )
    offset = fields.Integer(
        allow_none=True,
        dump_default=0,
        load_default=0,
    )

    class Meta:
        ordered = True
        unknown = EXCLUDE


class VendorPostInputSchema(Schema):
    category = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(allow_none=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class VendorPutInputSchema(Schema):
    item_id = fields.Integer(required=True)
    category = fields.String(allow_none=True)
    name = fields.String(allow_none=True)
    description = fields.String(allow_none=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class VendorDeleteInputSchema(Schema):
    item_id_list = fields.List(
        fields.Integer(),
        required=True,
    )

    class Meta:
        ordered = True
        unknown = EXCLUDE


class VendorDetailGetInputSchema(Schema):
    id = fields.String(required=True)

    class Meta:
        ordered = True
        unknown = EXCLUDE
