import sqlalchemy as sa
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import BaseModel


class Vendor(BaseModel):
    __tablename__ = "vendors"

    id = sa.Column(sa.String(20), primary_key=True)
    reference_id = sa.Column(sa.Integer(), sa.ForeignKey("references.id"), nullable=False)

    # region: General Information
    name = sa.Column(sa.String(50), nullable=False)
    organization_type = sa.Column(sa.String(25))  # TODO: BUMN, dll. || dictionary -> Foreign Key
    business_type = sa.Column(sa.String(10))  # TODO: CV, PO, PD, PT
    business_type_name = sa.Column(sa.String(50))  # TODO DELETE: use Enum aja lah goblok
    service_type = sa.Column(sa.String(10))  # "Supplier" || "Others" || "Contractor"
    industry_type = sa.Column(sa.String(100))
    service_specification = sa.Column(sa.String(120))
    service_description = sa.Column(sa.String(500))
    organization_status = sa.Column(sa.Boolean(), default=True, server_default="true")
    relationship_type = sa.Column(sa.String(10))  # "Contract" || "Project"
    director_name = sa.Column(sa.String(50))
    # region TODO REFACTOR: into a separate table: `contacts`?
    first_contact_person_name = sa.Column(sa.String(100), nullable=False)
    first_contact_person_phone = sa.Column(sa.String(100))
    first_contact_person_email = sa.Column(sa.String(200), nullable=False)
    second_contact_person_name = sa.Column(sa.String(100))
    second_contact_person_phone = sa.Column(sa.String(100))
    second_contact_person_email = sa.Column(sa.String(200))
    third_contact_person_name = sa.Column(sa.String(100))
    third_contact_person_phone = sa.Column(sa.String(100))
    third_contact_person_email = sa.Column(sa.String(200))
    # endregion
    # endregion

    # region: Address
    # TODO REFACTOR: `master_cities`, `master_provinces`, `master_countries`, `master_postal_codes`
    first_address = sa.Column(sa.String(200))
    first_city = sa.Column(sa.String(50))
    first_province = sa.Column(sa.String(35))
    first_country = sa.Column(sa.String(35))
    first_postal_code = sa.Column(sa.String(10))
    second_address = sa.Column(sa.String(200))
    second_city = sa.Column(sa.String(50))
    second_province = sa.Column(sa.String(35))
    second_country = sa.Column(sa.String(35))
    second_postal_code = sa.Column(sa.String(10))

    phone_number = sa.Column(sa.String(50))
    fax_number = sa.Column(sa.String(50))
    website = sa.Column(sa.String(100))
    # endregion

    # region: Employees and Fasilities
    employee_count = sa.Column(sa.BigInteger())
    management_count = sa.Column(sa.BigInteger())
    administration_count = sa.Column(sa.BigInteger())
    technician_count = sa.Column(sa.BigInteger())
    sales_count = sa.Column(sa.BigInteger())
    quality_assurance_count = sa.Column(sa.BigInteger())
    quality_control_count = sa.Column(sa.BigInteger())
    branch_count = sa.Column(sa.BigInteger())

    office_area = sa.Column(sa.Numeric(precision=18, scale=2), default=0)
    office_area_file = sa.Column(sa.String(10485760))
    warehouse_area = sa.Column(sa.Numeric(precision=18, scale=2), default=0)
    warehouse_area_file = sa.Column(sa.String(10485760))
    manufacture_area = sa.Column(sa.Numeric(precision=18, scale=2), default=0)
    manufacture_area_file = sa.Column(sa.String(10485760))
    others_area = sa.Column(sa.Numeric(precision=18, scale=2), default=0)
    others_area_file = sa.Column(sa.String(10485760))
    # endregion

    # region: Bank Account & Finance
    currency = sa.Column(sa.String(10), nullable=False)
    bank_name = sa.Column(sa.String(50), nullable=False)
    bank_branch = sa.Column(sa.String(50), nullable=False)
    bank_city = sa.Column(sa.String(25), nullable=False)
    bank_account_name = sa.Column(sa.String(50), nullable=False)
    bank_account_number = sa.Column(sa.String(30), nullable=False)
    authorized_capital = sa.Column(sa.BigInteger(), default=0)
    financial_ability = sa.Column(sa.BigInteger(), default=0)
    asset_count = sa.Column(sa.BigInteger(), default=0)
    niat = sa.Column(sa.Numeric(38, 2), default=0)  # NOTE: Net Income After Taxes
    ebitda = sa.Column(sa.Numeric(38, 2), default=0)  # NOTE: Earnings Before Interest, Taxes, Depreciation, and Amortization
    annual_revenue = sa.Column(sa.Numeric(38, 2), default=0)
    average_revenue = sa.Column(sa.Numeric(38, 2), default=0)
    # endregion

    # region: Legality Documents
    npwp_number = sa.Column(sa.String(30))
    npwp_file = sa.Column(sa.String(10485760))
    jamsostek_number = sa.Column(sa.String(100))
    jamsostek_file = sa.Column(sa.String(10485760))

    business_establishment_deed_number = sa.Column(sa.String(30))  # akta pendirian usaha
    business_establishment_deed_date = sa.Column(sa.DateTime(timezone=True))
    business_establishment_deed_file = sa.Column(sa.String(10485760))

    siup_number = sa.Column(sa.String(100))
    siup_type = sa.Column(sa.String(20))  # TODO: -, Kecil, Menengah, Besar
    siup_file = sa.Column(sa.String(10485760))

    nib_number = sa.Column(sa.String(100))
    nib_expiration_date = sa.Column(sa.DateTime(timezone=True))
    nib_file = sa.Column(sa.String(10485760))
    siujk = sa.Column(sa.String(100))
    siujk_grade = sa.Column(sa.String(10))
    siujk_expiration_date = sa.Column(sa.DateTime(timezone=True))
    siujk_file = sa.Column(sa.String(10485760))

    sbujpk_number = sa.Column(sa.String(100))
    sbujpk_grade = sa.Column(sa.String(100))
    sbujpk_expiration_date = sa.Column(sa.DateTime(timezone=True))
    sbujk_file = sa.Column(sa.String(10485760))

    iup_number = sa.Column(sa.String(100))
    iup_file = sa.Column(sa.String(10485760))
    sku_number = sa.Column(sa.String(100))
    sku_expiration_date = sa.Column(sa.DateTime(timezone=True))
    sku_file = sa.Column(sa.String(10485760))
    skdp_number = sa.Column(sa.String(100))
    skdp_expiration_date = sa.Column(sa.DateTime(timezone=True))
    skdp_file = sa.Column(sa.String(10485760))

    situ_number = sa.Column(sa.String(100))
    situ_expiration_date = sa.Column(sa.DateTime(timezone=True))
    situ_file = sa.Column(sa.String(10485760))

    sppkp_number = sa.Column(sa.String(100))
    sppkp_file = sa.Column(sa.String(10485760))

    skt_number = sa.Column(sa.String(100))
    skt_file = sa.Column(sa.String(10485760))

    tdp_number = sa.Column(sa.String(100))
    tdp_file = sa.Column(sa.String(10485760))
    # endregion

    # region: Additional Information
    qualification = sa.Column(sa.String(10))  # TODO: -, Kecil, Menengah, Besarr
    referenced_by = sa.Column(sa.String(30))
    kadin_number = sa.Column(sa.String(100))
    kadin_file = sa.Column(sa.String(10485760))
    sknkp_number = sa.Column(sa.String(100))
    sknkp_file = sa.Column(sa.String(10485760))
    other_document = sa.Column(sa.String(100))
    other_document_file = sa.Column(sa.String(10485760))
    # endregion

    ippkp = sa.Column("ippkp", sa.String(10485760))
    ipctf = sa.Column("ipctf", sa.String(10485760))
    ipcpf = sa.Column("ipcpf", sa.String(10485760))
    iporc = sa.Column("iporc", sa.String(10485760))
    ipctr = sa.Column("ipctr", sa.String(10485760))
    ipjex = sa.Column("ipjex", sa.String(10485760))
    iplot = sa.Column("iplot", sa.String(10485760))
    ipcsm = sa.Column("ipcsm", sa.String(10485760))
    ippmt = sa.Column("ippmt", sa.String(10485760))

    regsn = sa.Column("regsn", sa.String(50))
    compr = sa.Column("compr", sa.Boolean(), default=True, server_default="true")
    lglty = sa.Column("lglty", sa.Boolean(), default=True, server_default="true")
    visit = sa.Column("visit", sa.Boolean(), default=True, server_default="true")
    vassk = sa.Column("vassk", sa.String(30))
    vabss = sa.Column("vabss", sa.String(30))
    vakms = sa.Column("vakms", sa.String(30))
    fmads = sa.Column("fmads", sa.String(100))
    coacd = sa.Column("coacd", sa.String(20))
    coaat = sa.Column("coaat", sa.String(20))
    orgct = sa.Column("orgct", sa.String(10))
    qsysm = sa.Column("qsysm", sa.String(255))
    qsysa = sa.Column("qsysa", sa.String(255))
    is_agr = sa.Column("isagr", sa.Boolean(), default=True, server_default="true")
    grpcd = sa.Column("grpcd", sa.String(10))

    flag1 = sa.Column(sa.String(15))
    flag2 = sa.Column(sa.String(15))
    temps = sa.Column(sa.String(100))
    is_active = sa.Column(sa.Boolean(), default=True, server_default="true")

    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
