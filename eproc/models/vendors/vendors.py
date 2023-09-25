import sqlalchemy as sa
from sqlalchemy.orm import backref, column_property
from sqlalchemy.sql import case

from eproc import db
from eproc.models.base_model import BaseModel


class Vendor(BaseModel):
    __tablename__ = "vendors"

    # region: General Information
    id = sa.Column(sa.String(), primary_key=True)
    name = sa.Column("vdrnm", sa.String(), nullable=False)
    organization_type = sa.Column("orgty", sa.String())  # TODO: BUMN, dll. || dictionary -> Foreign Key
    business_type = sa.Column("bnsty", sa.String())  # TODO: CV, PO, PD, PT
    business_type_name = sa.Column("bnsnm", sa.String())  # TODO DELETE: use Enum aja lah goblok
    service_type = sa.Column("svcty", sa.String())  # "Supplier" || "Others" || "Contractor"
    industry_type = sa.Column("spcty", sa.String())
    service_specification = sa.Column("specn", sa.String())
    service_description = sa.Column("orsvc", sa.String())
    organization_status = sa.Column("orgst", sa.String())
    relationship_type = sa.Column("costt", sa.String())  # "Contract" || "Project"
    director_name = sa.Column("drctr", sa.String())

    # region TODO REFACTOR: into a separate table: `contacts`?
    first_contact_person_name = sa.Column("ctpn1", sa.String(), nullable=False)
    first_contact_person_phone = sa.Column("ctph1", sa.String())
    first_contact_person_email = sa.Column("ctem1", sa.String(), nullable=False)
    second_contact_person_name = sa.Column("ctpn2", sa.String())
    second_contact_person_phone = sa.Column("ctph2", sa.String())
    second_contact_person_email = sa.Column("ctem2", sa.String())
    third_contact_person_name = sa.Column("ctpn3", sa.String())
    third_contact_person_phone = sa.Column("ctph3", sa.String())
    third_contact_person_email = sa.Column("ctem3", sa.String())
    # endregion
    # endregion

    # region: Address
    # TODO REFACTOR: `master_cities`, `master_provinces`, `master_countries`, `master_postal_codes`
    first_address = sa.Column("addr1", sa.String())
    first_city = sa.Column("city1", sa.String())
    first_province = sa.Column("prvc1", sa.String())
    first_country = sa.Column("cntr1", sa.String())
    first_postal_code = sa.Column("pcod1", sa.String())
    second_address = sa.Column("addr2", sa.String())
    second_city = sa.Column("city2", sa.String())
    second_province = sa.Column("prvc2", sa.String())
    second_country = sa.Column("cntr2", sa.String())
    second_postal_code = sa.Column("pcod2", sa.String())

    phone_number = sa.Column("phone", sa.String())
    fax_number = sa.Column("faxno", sa.String())
    website = sa.Column("webst", sa.String())
    # endregion

    # region: Employees and Fasilities
    employee_count = sa.Column("noemp", sa.Integer())
    management_count = sa.Column("nomgm", sa.Integer())
    administration_count = sa.Column("noadm", sa.Integer())
    technician_count = sa.Column("notch", sa.Integer())
    sales_count = sa.Column("nosls", sa.Integer())
    quality_assurance_count = sa.Column("noqas", sa.Integer())
    quality_control_count = sa.Column("noqcl", sa.Integer())
    branch_count = sa.Column("nobrc", sa.Integer())

    office_area = sa.Column("sooff", sa.Numeric(precision=18, scale=2), default=0)
    office_area_file = sa.Column("ipoff", sa.String(10485760))
    warehouse_area = sa.Column("sowhs", sa.Numeric(precision=18, scale=2), default=0)
    warehouse_area_file = sa.Column("ipwhs", sa.String(10485760))
    manufacture_area = sa.Column("somfr", sa.Numeric(precision=18, scale=2), default=0)
    manufacture_area_file = sa.Column("ipmfr", sa.String(10485760))
    others_area = sa.Column("sooth", sa.Numeric(precision=18, scale=2), default=0)
    others_area_file = sa.Column("ipoth", sa.String(10485760))
    # endregion

    # region: Bank Account & Finance
    currency = sa.Column("curcd", sa.String(), nullable=False)
    bank_name = sa.Column("zbank", sa.String(), nullable=False)
    bank_branch = sa.Column("bbank", sa.String(), nullable=False)
    bank_city = sa.Column("cbank", sa.String(), nullable=False)
    bank_account_name = sa.Column("nbank", sa.String(), nullable=False)
    bank_account_number = sa.Column("rbank", sa.String(), nullable=False)
    authorized_capital = sa.Column("incap", sa.BigInteger(), default=0)
    financial_ability = sa.Column("finab", sa.BigInteger(), default=0)
    asset_count = sa.Column("noast", sa.BigInteger(), default=0)
    niat = sa.Column("nniat", sa.Numeric(38, 2), default=0)  # NOTE: Net Income After Taxes
    ebitda = sa.Column("ebitd", sa.Numeric(38, 2), default=0)  # NOTE: Earnings Before Interest, Taxes, Depreciation, and Amortization
    annual_revenue = sa.Column("annrv", sa.Numeric(38, 2), default=0)
    average_revenue = sa.Column("avarv", sa.Numeric(38, 2), default=0)
    # endregion

    # region: Legality Documents
    npwp_number = sa.Column("nnpwp", sa.String())
    npwp_file = sa.Column("inpwp", sa.String(10485760))
    jamsostek_number = sa.Column("njstk", sa.String())
    jamsostek_file = sa.Column("ijstk", sa.String(10485760))

    business_establishment_deed_number = sa.Column("nakta", sa.String())  # akta pendirian usaha
    business_establishment_deed_date = sa.Column("dakta", sa.DateTime(), default=None)
    business_establishment_deed_file = sa.Column("iakta", sa.String(10485760))

    siup_number = sa.Column("nsiup", sa.String())
    siup_type = sa.Column("tsiup", sa.String())  # TODO: -, Kecil, Menengah, Besar
    siup_file = sa.Column("isiup", sa.String(10485760))

    nib = sa.Column("nbnib", sa.String())
    nib_expiration_date = sa.Column("expd1", sa.DateTime())
    nbnib_file = sa.Column("ipnib", sa.String(10485760))
    siujk = sa.Column("siujk", sa.String())
    siujk_grade = sa.Column("grde1", sa.String())
    siujk_expiration_date = sa.Column("expd3", sa.DateTime())
    siujk_file = sa.Column("isiuj", sa.String(10485760))

    sbujpk_number = sa.Column("sbujp", sa.String())
    sbujpk_grade = sa.Column("grde2", sa.String())
    sbujpk_expiration_date = sa.Column("expd4", sa.DateTime())
    sbujk_file = sa.Column("isbuj", sa.String(10485760))

    iup_number = sa.Column("nbiup", sa.String())
    iup_file = sa.Column("ipiup", sa.String(10485760))
    sku_number = sa.Column("nbsku", sa.String())
    sku_expiration_date = sa.Column("expd6", sa.DateTime())
    sku_file = sa.Column("ipsku", sa.String(10485760))
    skdp_number = sa.Column("nskdp", sa.String())
    skdp_expiration_date = sa.Column("expd2", sa.DateTime())
    skdp_file = sa.Column("iskdp", sa.String(10485760))

    situ_number = sa.Column("nsitu", sa.String())
    situ_expiration_date = sa.Column("expd5", sa.DateTime())
    situ_file = sa.Column("isitu", sa.String(10485760))

    sppkp_number = sa.Column("sppkp", sa.String())
    sppkp_file = sa.Column("isppk", sa.String(10485760))

    skt_number = sa.Column("nbskt", sa.String())
    skt_file = sa.Column("ipskt", sa.String(10485760))

    tdp_number = sa.Column("nbtdp", sa.String())
    tdp_file = sa.Column("iptdp", sa.String(10485760))
    # endregion

    # region: Additional Information
    qualification = sa.Column("qfctn", sa.String())  # TODO: -, Kecil, Menengah, Besarr
    referenced_by = sa.Column("refri", sa.String())
    kadin_number = sa.Column("kadin", sa.String())
    kadin_file = sa.Column("ikdin", sa.String(10485760))
    sknkp_number = sa.Column("sknkp", sa.String())
    sknkp_file = sa.Column("iknkp", sa.String(10485760))
    other_document = sa.Column("otdoc", sa.String())
    other_document_file = sa.Column("iotdc", sa.String(10485760))
    # endregion

    reference_id = sa.Column("stats", sa.Integer(), sa.ForeignKey("references.id"))

    ippkp = sa.Column("ippkp", sa.String(10485760))
    ipctf = sa.Column("ipctf", sa.String(10485760))
    ipcpf = sa.Column("ipcpf", sa.String(10485760))
    iporc = sa.Column("iporc", sa.String(10485760))
    ipctr = sa.Column("ipctr", sa.String(10485760))
    ipjex = sa.Column("ipjex", sa.String(10485760))
    iplot = sa.Column("iplot", sa.String(10485760))
    ipcsm = sa.Column("ipcsm", sa.String(10485760))
    ippmt = sa.Column("ippmt", sa.String(10485760))

    regsn = sa.Column("regsn", sa.String())
    compr = sa.Column("compr", sa.Integer(), default=0)  # TODO: change to boolean
    lglty = sa.Column("lglty", sa.Integer(), default=0)  # TODO: change to boolean
    visit = sa.Column("visit", sa.Integer(), default=0)  # TODO: change to boolean
    vassk = sa.Column("vassk", sa.String())
    vabss = sa.Column("vabss", sa.String())
    vakms = sa.Column("vakms", sa.String())
    fmads = sa.Column("fmads", sa.String())
    coacd = sa.Column("coacd", sa.String())
    coaat = sa.Column("coaat", sa.String())
    flag1 = sa.Column("flag1", sa.String())
    flag2 = sa.Column("flag2", sa.String())
    temps = sa.Column("temps", sa.String())
    orgct = sa.Column("orgct", sa.String())
    qsysm = sa.Column("qsysm", sa.String())
    qsysa = sa.Column("qsysa", sa.String())
    isagr = sa.Column("isagr", sa.Integer(), default=0)  # TODO: change to boolean
    grpcd = sa.Column("grpcd", sa.String())

    isact = sa.Column("isact", sa.Integer(), default=0)  # TODO: change to boolean
    is_active = column_property(
        case((isact == 1, True), else_=False)
    )

    reference = db.relationship(
        "Reference", backref=backref(__tablename__, uselist=False)
    )
