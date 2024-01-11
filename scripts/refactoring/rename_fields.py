import psycopg2
from traceback import format_exc
from typing import List

from constants import to_be_renamed_tables


def get_connection_and_cursor():
    DB_USER = "postgres"
    DB_PASS = "postgres123"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "eprocure_new"

    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
        )
        cursor = conn.cursor()
        return True, conn, cursor

    except Exception as e:
        # print(f"Error while trying to connect to DB :: {e}")
        return False, None, None


def execute(query: str):
    table = query.split()[2]
    if table != "table":
        try:
            cursor.execute(query)
            conn.commit()
            print(f"Success :: table: {table}")
        except Exception as e:
            conn.rollback()
            print(f"ERROR :: table: {table}, error: {e}")


def drop_default_if_exists(table_names: dict, field_name: str):
    error: List[str] = list()

    for table in table_names:
        if isinstance(table, dict):
            table = table_names.get(table) if table_names.get(table) else table
        try:
            execute(f"ALTER TABLE \"{table}\" ALTER COLUMN {field_name} DROP DEFAULT;")
        except:
            error.append(table)

    if error:
        print(f"drop_default_if_exists() :: field: {field_name}, error: {error}")

status, conn, cursor = get_connection_and_cursor()


if __name__ == "__main__":
    # from eproc_constants import to_be_renamed_tables
    # drop_default_if_exists(table_names=to_be_renamed_tables, field_name="updated_by")

    try:

        # region: table
        execute("ALTER TABLE table RENAME COLUMN old TO new")

        execute(
            """
            ALTER TABLE table
            ALTER COLUMN is_active TYPE boolean
            USING CASE WHEN is_active::integer = 1 THEN TRUE ELSE FALSE END;
            """
        )
        execute(
            """
            ALTER TABLE table
            ALTER COLUMN is_active TYPE BOOLEAN USING is_active::INTEGER::BOOLEAN;
            """
        )




        execute(
            """
            ALTER TABLE table
            ALTER COLUMN is_active DROP DEFAULT,
            ALTER COLUMN is_active TYPE BOOLEAN USING is_active::INTEGER::BOOLEAN;

            ALTER TABLE table
            ALTER COLUMN is_active SET DEFAULT TRUE;
            """
        )



        # NOTE: change `id` to auto-incremental
        # execute("""
        #     CREATE SEQUENCE table_id_seq
        #     OWNED BY table.id;

        #     ALTER TABLE table
        #     ALTER COLUMN id SET DEFAULT nextval('table_id_seq');
        # """)
        # endregion: table


        # region: group: masters
        # region: entities
        # query = (
        #     """
        #     ALTER TABLE entities
        #     RENAME COLUMN descr TO description;

        #     ALTER TABLE entities
        #     RENAME COLUMN isact TO is_active;

        #     """
        # )
        # execute(query)

        # query = (
        #     """
        #     ALTER TABLE entities
        #     ALTER COLUMN is_active TYPE boolean
        #     USING CASE WHEN is_active::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # execute(query)
        # endregion: entities

        # region: regionals
    #     execute("ALTER TABLE regionals RENAME COLUMN rgnid TO id")
    #     query = (
    #         """
    #         ALTER TABLE regionals
    #         RENAME COLUMN isact TO is_active;

    #         ALTER TABLE regionals
    #         RENAME COLUMN descr TO description;
            
    #         ALTER TABLE regionals
    #         RENAME COLUMN nttid TO entity_id;

    #         ALTER TABLE regionals
    #         RENAME COLUMN addl1 TO first_address;

    #         ALTER TABLE regionals
    #         RENAME COLUMN addl2 TO second_address;

    #         ALTER TABLE regionals
    #         RENAME COLUMN addl3 TO third_address;

    #         ALTER TABLE regionals
    #         RENAME COLUMN ocity TO city;

    #         ALTER TABLE regionals
    #         RENAME COLUMN provc TO province;

    #         ALTER TABLE regionals
    #         RENAME COLUMN cntry TO country;

    #         ALTER TABLE regionals
    #         RENAME COLUMN phone TO phone_number;

    #         ALTER TABLE regionals
    #         RENAME COLUMN nofax TO fax_number;

    #         """
    #     )
    #     execute(query)

    #     query = (
    #         """
    #         ALTER TABLE regionals
    #         ALTER COLUMN is_active TYPE boolean
    #         USING CASE WHEN is_active::integer = 1 THEN TRUE ELSE FALSE END;
    #         """
    #     )
    #     execute(query)
        # endregion: regionals
        
        # region: references
        # execute("ALTER TABLE \"references\" RENAME COLUMN cdnum TO id;")
        # # execute("ALTER TABLE \"references\" RENAME COLUMN refid TO ;")
        # execute("ALTER TABLE \"references\" RENAME COLUMN cdval TO parameter_value;")
        # execute("ALTER TABLE \"references\" RENAME COLUMN cdtxt TO parameter_text;")
        # execute("ALTER TABLE \"references\" RENAME COLUMN descr TO description;")
        # execute("ALTER TABLE \"references\" RENAME COLUMN zordr TO order_number;")
        # # execute("ALTER TABLE \"references\" RENAME COLUMN rsign TO ;")
        # # execute("ALTER TABLE \"references\" RENAME COLUMN dref1 TO ;")
        # # execute("ALTER TABLE \"references\" RENAME COLUMN dref2 TO ;")
        # # execute("ALTER TABLE \"references\" RENAME COLUMN dref3 TO ;")
        # execute("ALTER TABLE \"references\" RENAME COLUMN isact TO is_active;")
        # execute(
        #     """
        #     ALTER TABLE \"references\"
        #     ALTER COLUMN is_active DROP DEFAULT,
        #     ALTER COLUMN is_active TYPE BOOLEAN USING is_active::INTEGER::BOOLEAN;

        #     ALTER TABLE \"references\"
        #     ALTER COLUMN is_active SET DEFAULT TRUE;
        #     """
        # )
        # endregion: references

        # region: currencies
        # execute("ALTER TABLE currencies RENAME COLUMN curcd TO id;")
        # execute("ALTER TABLE currencies RENAME COLUMN descr TO description;")
        # execute("""
        #     ALTER TABLE currencies
        #     ALTER COLUMN description DROP DEFAULT,
        #     ALTER COLUMN description DROP NOT NULL;
        # """)
        # execute("ALTER TABLE currencies RENAME COLUMN cursb TO symbol;")
        # execute("""
        #     ALTER TABLE currencies ALTER COLUMN symbol DROP DEFAULT;
        #     ALTER TABLE currencies ALTER COLUMN symbol DROP NOT NULL;
        # """)

        # execute(
        #     """
        #     ALTER TABLE currencies
        #     ALTER COLUMN isbsc DROP DEFAULT,
        #     ALTER COLUMN isbsc TYPE BOOLEAN USING isbsc::INTEGER::BOOLEAN;

        #     ALTER TABLE currencies ALTER COLUMN isbsc SET DEFAULT FALSE;
        #     """
        # )
        # # execute("ALTER TABLE currencies RENAME COLUMN isbsc TO ;")

        # execute("ALTER TABLE currencies RENAME COLUMN isact TO is_active;")
        # execute(
        #     """
        #     ALTER TABLE currencies
        #     ALTER COLUMN is_active DROP DEFAULT,
        #     ALTER COLUMN is_active TYPE BOOLEAN USING is_active::INTEGER::BOOLEAN;

        #     ALTER TABLE currencies ALTER COLUMN is_active SET DEFAULT TRUE;
        #     """
        # )
        # endregion: currencies

        # endregion: group: masters

        # region: group: auth
        # region: roles
        # execute("ALTER TABLE roles RENAME COLUMN descr TO description;")
        # execute("ALTER TABLE roles RENAME COLUMN isact TO is_active;")

        # execute(
        #     """
        #     ALTER TABLE roles
        #     ALTER COLUMN is_active TYPE boolean
        #     USING CASE WHEN is_active::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # endregion: roles

        # region: user_roles
        # execute("ALTER TABLE user_roles RENAME COLUMN usrid TO user_id;")
        # execute("ALTER TABLE user_roles RENAME COLUMN rolid TO role_id;")
        # endregion: user_roles

        # region: branch_roles
        # execute("ALTER TABLE branch_roles RENAME COLUMN brcid TO branch_id;")
        # execute("ALTER TABLE branch_roles RENAME COLUMN rolid TO role_id;")
        # endregion: branch_roles

        # region: menus
        # execute("ALTER TABLE menus RENAME COLUMN mnuid TO id;")
        # execute("ALTER TABLE menus RENAME COLUMN mdlid TO module_id;")
        # execute("ALTER TABLE menus RENAME COLUMN appid TO app_id;")
        # execute("ALTER TABLE menus RENAME COLUMN mnunm TO menu_name;")
        # execute("ALTER TABLE menus RENAME COLUMN mnutx TO menu_tag;")
        # execute("ALTER TABLE menus RENAME COLUMN levlz TO level;")
        # execute("ALTER TABLE menus RENAME COLUMN prnid TO parent_id;")
        # # execute("ALTER TABLE menus RENAME COLUMN clasz TO ;")
        # # execute("ALTER TABLE menus RENAME COLUMN cntlr TO ;")
        # execute("ALTER TABLE menus RENAME COLUMN actns TO action;")
        # execute("ALTER TABLE menus RENAME COLUMN actur TO action_url;")
        # execute("ALTER TABLE menus RENAME COLUMN iconz TO icon;")
        # # execute("ALTER TABLE menus RENAME COLUMN lstid TO ;")
        # # execute("ALTER TABLE menus RENAME COLUMN regfl TO ;")
        # # execute("ALTER TABLE menus RENAME COLUMN appfl TO ;")
        # # execute("ALTER TABLE menus RENAME COLUMN rejfl TO ;")
        # execute("ALTER TABLE menus RENAME COLUMN sqenc TO sequence_number;")

        # NOTE: bersihin isi tabel yang empty string
        # execute("UPDATE menus SET prnid = NULL WHERE prnid = '';")
        # execute("ALTER TABLE menus RENAME COLUMN isact TO is_active;")

        # execute(
        #     """
        #     ALTER TABLE menus
        #     ALTER COLUMN is_active TYPE boolean
        #     USING CASE WHEN is_active::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE menus
        #     ALTER COLUMN appif TYPE boolean
        #     USING CASE WHEN appif::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # # execute("ALTER TABLE menus RENAME COLUMN appif TO ;")
        # execute(
        #     """
        #     ALTER TABLE menus
        #     ALTER COLUMN isprn TYPE boolean
        #     USING CASE WHEN isprn::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # execute("ALTER TABLE menus RENAME COLUMN isprn TO is_parent;")
        # endregion: menus

        # region: roles_menus
        # execute("ALTER TABLE roles_menus RENAME COLUMN mnuid TO menu_id;")
        # execute("ALTER TABLE roles_menus RENAME COLUMN rolid TO role_id;")

        # execute(
        #     """
        #     ALTER TABLE roles_menus
        #     ALTER COLUMN aladd TYPE boolean
        #     USING CASE WHEN aladd::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE roles_menus
        #     ALTER COLUMN aledt TYPE boolean
        #     USING CASE WHEN aledt::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE roles_menus
        #     ALTER COLUMN aldel TYPE boolean
        #     USING CASE WHEN aldel::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE roles_menus
        #     ALTER COLUMN alexc TYPE boolean
        #     USING CASE WHEN alexc::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE roles_menus
        #     ALTER COLUMN alsnc TYPE boolean
        #     USING CASE WHEN alsnc::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE roles_menus
        #     ALTER COLUMN alpos TYPE boolean
        #     USING CASE WHEN alpos::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE roles_menus
        #     ALTER COLUMN alups TYPE boolean
        #     USING CASE WHEN alups::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE roles_menus
        #     ALTER COLUMN alaap TYPE boolean
        #     USING CASE WHEN alaap::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE roles_menus
        #     ALTER COLUMN alapp TYPE boolean
        #     USING CASE WHEN alapp::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE roles_menus
        #     ALTER COLUMN alrej TYPE boolean
        #     USING CASE WHEN alrej::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE roles_menus
        #     ALTER COLUMN altsk DROP DEFAULT,
        #     ALTER COLUMN altsk TYPE BOOLEAN USING altsk::INTEGER::BOOLEAN;

        #     ALTER TABLE roles_menus ALTER COLUMN altsk SET DEFAULT FALSE;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE roles_menus
        #     ALTER COLUMN alprn DROP DEFAULT,
        #     ALTER COLUMN alprn TYPE BOOLEAN USING alprn::INTEGER::BOOLEAN;

        #     ALTER TABLE roles_menus ALTER COLUMN alprn SET DEFAULT FALSE;
        #     """
        # )
        # endregion: roles_menus
        # endregion: group: auth

        # region: group: users
        # region: users
        # execute(
        #     """
        #     ALTER TABLE users
        #     RENAME COLUMN stats TO reference_id;
        #     """
        # )

        # execute("ALTER TABLE users RENAME COLUMN ldid1 TO first_approver_id;")
        # execute("ALTER TABLE users RENAME COLUMN ldid2 TO second_approver_id;")
        # execute("ALTER TABLE users RENAME COLUMN ldid3 TO third_approver_id;")

        # execute("ALTER TABLE users RENAME COLUMN appid TO app_id;")
        # execute("ALTER TABLE users RENAME COLUMN uname TO username;")
        # execute("ALTER TABLE users RENAME COLUMN ffnam TO full_name;")
        # execute("ALTER TABLE users RENAME COLUMN paswd TO password;")
        # execute("ALTER TABLE users RENAME COLUMN pasfm TO password_length;")
        # execute("ALTER TABLE users RENAME COLUMN passt TO password_salt;")
        # execute("ALTER TABLE users RENAME COLUMN pashs TO clear_text_password;")
        # execute("ALTER TABLE users RENAME COLUMN pasqs TO password_question;")
        # execute("ALTER TABLE users RENAME COLUMN pasaw TO password_answer;")
        # execute("ALTER TABLE users RENAME COLUMN secst TO security_status;")

        # execute("ALTER TABLE users RENAME COLUMN isact TO is_active;")
        # execute("ALTER TABLE users RENAME COLUMN emcon TO is_email_confirmed;")
        # execute("ALTER TABLE users RENAME COLUMN isann TO is_anonymous;")
        # execute("ALTER TABLE users RENAME COLUMN isadm TO is_admin;")
        # execute("ALTER TABLE users RENAME COLUMN isuho TO is_head_office_user;")
        # execute("ALTER TABLE users RENAME COLUMN isukp TO is_kpw_user;")
        # execute("ALTER TABLE users RENAME COLUMN isust TO is_branch_user;")
        # execute("ALTER TABLE users RENAME COLUMN isapr TO is_approved;")
        # execute("ALTER TABLE users RENAME COLUMN islck TO is_locked;")
        # execute("ALTER TABLE users RENAME COLUMN remme TO remember_me;")
        # execute("ALTER TABLE users RENAME COLUMN phonc TO is_phone_number_confirmed;")
        # execute("ALTER TABLE users RENAME COLUMN tface TO two_factor_enabled;")
        # execute("ALTER TABLE users RENAME COLUMN locen TO lock_enabled;")
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN is_active DROP DEFAULT,
        #     ALTER COLUMN is_active TYPE BOOLEAN USING is_active::INTEGER::BOOLEAN;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN is_email_confirmed DROP DEFAULT,
        #     ALTER COLUMN is_email_confirmed TYPE BOOLEAN USING is_email_confirmed::INTEGER::BOOLEAN;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN is_anonymous DROP DEFAULT,
        #     ALTER COLUMN is_anonymous TYPE BOOLEAN USING is_anonymous::INTEGER::BOOLEAN;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN is_admin DROP DEFAULT,
        #     ALTER COLUMN is_admin TYPE BOOLEAN USING is_admin::INTEGER::BOOLEAN;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN is_head_office_user DROP DEFAULT,
        #     ALTER COLUMN is_head_office_user TYPE BOOLEAN USING is_head_office_user::INTEGER::BOOLEAN;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN is_kpw_user DROP DEFAULT,
        #     ALTER COLUMN is_kpw_user TYPE BOOLEAN USING is_kpw_user::INTEGER::BOOLEAN;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN is_branch_user DROP DEFAULT,
        #     ALTER COLUMN is_branch_user TYPE BOOLEAN USING is_branch_user::INTEGER::BOOLEAN;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN is_approved DROP DEFAULT,
        #     ALTER COLUMN is_approved TYPE BOOLEAN USING is_approved::INTEGER::BOOLEAN;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN is_locked DROP DEFAULT,
        #     ALTER COLUMN is_locked TYPE BOOLEAN USING is_locked::INTEGER::BOOLEAN;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN remember_me DROP DEFAULT,
        #     ALTER COLUMN remember_me TYPE BOOLEAN USING remember_me::INTEGER::BOOLEAN;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN is_phone_number_confirmed DROP DEFAULT,
        #     ALTER COLUMN is_phone_number_confirmed TYPE BOOLEAN USING is_phone_number_confirmed::INTEGER::BOOLEAN;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN two_factor_enabled DROP DEFAULT,
        #     ALTER COLUMN two_factor_enabled TYPE BOOLEAN USING two_factor_enabled::INTEGER::BOOLEAN;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN lock_enabled DROP DEFAULT,
        #     ALTER COLUMN lock_enabled TYPE BOOLEAN USING lock_enabled::INTEGER::BOOLEAN;
        #     """
        # )
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN acfct DROP DEFAULT,
        #     ALTER COLUMN acfct TYPE BOOLEAN USING acfct::INTEGER::BOOLEAN;
        #     """
        # )

        # execute("ALTER TABLE users RENAME COLUMN sapsa TO captcha;")
        # execute("ALTER TABLE users RENAME COLUMN mopin TO mobile_pin;")
        # execute("ALTER TABLE users RENAME COLUMN moals TO mobile_alias;")

        # execute("ALTER TABLE users RENAME COLUMN ladat TO last_active_date;")
        # execute("ALTER TABLE users RENAME COLUMN llgdt TO last_login_date;")
        # execute("ALTER TABLE users RENAME COLUMN llkdt TO last_lock_date;")
        # execute(
        #     """
        #     ALTER TABLE users
        #     ALTER COLUMN last_lock_date DROP DEFAULT,
        #     ALTER COLUMN last_lock_date DROP NOT NULL;
        #     """
        # )
        # execute("ALTER TABLE users RENAME COLUMN lpcdt TO last_password_change_date;")

        # execute("ALTER TABLE users RENAME COLUMN comnt TO comment;")
        # execute("ALTER TABLE users RENAME COLUMN phono TO phone_number;")
        # execute("ALTER TABLE users RENAME COLUMN loced TO valid_until;")
        # endregion: users

        # region: employees
        # execute("ALTER TABLE employees RENAME COLUMN isact TO is_active;")
        # execute("ALTER TABLE employees RENAME COLUMN rgnid TO regional_id;")
        # execute("ALTER TABLE employees RENAME COLUMN nttid TO entity_id;")
        # execute("ALTER TABLE employees RENAME COLUMN brcid TO branch_id;")
        # execute("ALTER TABLE employees RENAME COLUMN dirid TO directorate_id;")
        # execute("ALTER TABLE employees RENAME COLUMN divid TO division_id;")
        # execute("ALTER TABLE employees RENAME COLUMN depid TO department_id;")
        # execute("ALTER TABLE employees RENAME COLUMN coacd to cost_center_id;")
        # execute("ALTER TABLE employees RENAME COLUMN empnm TO full_name;")
        # execute("ALTER TABLE employees RENAME COLUMN phone TO phone_number;")
        # execute("ALTER TABLE employees RENAME COLUMN noktp TO identity_number;")
        # execute("ALTER TABLE employees RENAME COLUMN gendr TO gender;")
        # execute("ALTER TABLE employees RENAME COLUMN joidt TO join_date;")
        # execute("ALTER TABLE employees RENAME COLUMN outdt TO leave_date;")
        # execute("ALTER TABLE employees RENAME COLUMN ldid1 TO first_approver_id;")
        # execute("ALTER TABLE employees RENAME COLUMN ldid2 TO second_approver_id;")
        # execute("ALTER TABLE employees RENAME COLUMN ldid3 TO third_approver_id;")
        # execute("ALTER TABLE employees RENAME COLUMN grpid TO group_id;")

        # execute(
        #     """
        #     ALTER TABLE employees
        #     ALTER COLUMN is_active DROP DEFAULT,
        #     ALTER COLUMN is_active TYPE BOOLEAN USING is_active::INTEGER::BOOLEAN;
        #     """
        # )
        # endregion: employees
        # endregion: group: users
        # region: group: companies
        # region: directorates
    #     query = (
    #         """
    #         ALTER TABLE directorates
    #         RENAME COLUMN descr TO description;

    #         ALTER TABLE directorates
    #         RENAME COLUMN nttid TO entity_id;

    #         ALTER TABLE directorates
    #         RENAME COLUMN isact TO is_active;

    #         """
    #     )
    #     execute(query)

    #     query = (
    #         """
    #         ALTER TABLE directorates
    #         ALTER COLUMN is_active TYPE boolean
    #         USING CASE WHEN is_active::integer = 1 THEN TRUE ELSE FALSE END;
    #         """
    #     )
    #     execute(query)
        # endregion: directorates

        # region: divisions
    #     query = (
    #         """
    #         ALTER TABLE divisions
    #         RENAME COLUMN descr TO description;

    #         ALTER TABLE divisions
    #         RENAME COLUMN nttid TO entity_id;

    #         ALTER TABLE divisions
    #         RENAME COLUMN isact TO is_active;

    #         """
    #     )
    #     execute(query)

    #     query = (
    #         """
    #         ALTER TABLE divisions
    #         ALTER COLUMN is_active TYPE boolean
    #         USING CASE WHEN is_active::integer = 1 THEN TRUE ELSE FALSE END;
    #         """
    #     )
    #     execute(query)
        # endregion: divisions

        # region: branches
    #     query = (
    #         """
    #         ALTER TABLE branches
    #         RENAME COLUMN isact TO is_active;

    #         ALTER TABLE branches
    #         RENAME COLUMN descr TO description;
            
    #         ALTER TABLE branches
    #         RENAME COLUMN nttid TO entity_id;

    #         ALTER TABLE branches
    #         RENAME COLUMN addl1 TO first_address;

    #         ALTER TABLE branches
    #         RENAME COLUMN addl2 TO second_address;

    #         ALTER TABLE branches
    #         RENAME COLUMN addl3 TO third_address;

    #         ALTER TABLE branches
    #         RENAME COLUMN ocity TO city;

    #         ALTER TABLE branches
    #         RENAME COLUMN provc TO province;

    #         ALTER TABLE branches
    #         RENAME COLUMN cntry TO country;

    #         ALTER TABLE branches
    #         RENAME COLUMN phone TO phone_number;

    #         ALTER TABLE branches
    #         RENAME COLUMN nofax TO fax_number;

    #         """
    #     )
    #     execute(query)

    #     query = (
    #         """
    #         ALTER TABLE branches
    #         ALTER COLUMN is_active TYPE boolean
    #         USING CASE WHEN is_active::integer = 1 THEN TRUE ELSE FALSE END;
    #         """
    #     )
    #     execute(query)
        # endregion: branches

        # region: departments
    #     query = (
    #         """
    #         ALTER TABLE departments
    #         RENAME COLUMN isact TO is_active;
            
    #         ALTER TABLE departments
    #         RENAME COLUMN descr TO description;

    #         ALTER TABLE departments
    #         RENAME COLUMN nttid TO entity_id;
    #         """
    #     )
    #     execute(query)

    #     query = (
    #         """
    #         ALTER TABLE departments
    #         ALTER COLUMN is_active TYPE boolean
    #         USING CASE WHEN is_active::integer = 1 THEN TRUE ELSE FALSE END;
    #         """
    #     )
    #     execute(query)
        # endregion: departments
        
        # region: groups
        # execute("ALTER TABLE groups RENAME COLUMN grpid TO id;")
        # execute("ALTER TABLE groups RENAME COLUMN descr TO description;")
        # execute("ALTER TABLE groups RENAME COLUMN nttid TO entity_id;")
        # execute("ALTER TABLE groups RENAME COLUMN isact TO is_active;")
        # execute(
        #     """
        #     ALTER TABLE groups
        #     ALTER COLUMN is_active TYPE boolean
        #     USING CASE WHEN is_active::integer = 1 THEN TRUE ELSE FALSE END;
        #     """
        # )
        # endregion: groups
        # endregion: group: companies

        # region: group: vendors
        # region: vendors
        # execute("ALTER TABLE vendors RENAME COLUMN vdrid TO id")
        # execute("ALTER TABLE vendors RENAME COLUMN stats TO reference_id")
        # execute("ALTER TABLE vendors RENAME COLUMN coacd to cost_center_id;")

    #     execute("ALTER TABLE vendors RENAME COLUMN vdrnm TO name")
    #     execute("ALTER TABLE vendors RENAME COLUMN orgty TO organization_type")
    #     execute("ALTER TABLE vendors RENAME COLUMN bnsty TO business_type")
    #     execute("ALTER TABLE vendors RENAME COLUMN bnsnm TO business_type_name")
    #     execute("ALTER TABLE vendors RENAME COLUMN svcty TO service_type")
    #     execute("ALTER TABLE vendors RENAME COLUMN spcty TO industry_type")
    #     execute("ALTER TABLE vendors RENAME COLUMN specn TO service_specification")
    #     execute("ALTER TABLE vendors RENAME COLUMN orsvc TO service_description")
    #     execute("ALTER TABLE vendors RENAME COLUMN orgst TO organization_status")
    #     execute(
    #         """
    #         ALTER TABLE vendors
    #         ALTER COLUMN organization_status DROP DEFAULT,
    #         ALTER COLUMN organization_status TYPE BOOLEAN USING organization_status::INTEGER::BOOLEAN;
    #         """
    #     )
    #     execute(
    #         """
    #         ALTER TABLE vendors
    #         ALTER COLUMN organization_status SET DEFAULT TRUE;
    #         """
    #     )
    #     execute("ALTER TABLE vendors RENAME COLUMN costt TO relationship_type")
    #     execute("ALTER TABLE vendors RENAME COLUMN drctr TO director_name")
    #     execute("ALTER TABLE vendors RENAME COLUMN ctpn1 TO first_contact_person_name")
    #     execute("ALTER TABLE vendors RENAME COLUMN ctph1 TO first_contact_person_phone")
    #     execute("ALTER TABLE vendors RENAME COLUMN ctem1 TO first_contact_person_email")
    #     execute("ALTER TABLE vendors RENAME COLUMN ctpn2 TO second_contact_person_name")
    #     execute("ALTER TABLE vendors RENAME COLUMN ctph2 TO second_contact_person_phone")
    #     execute("ALTER TABLE vendors RENAME COLUMN ctem2 TO second_contact_person_email")
    #     execute("ALTER TABLE vendors RENAME COLUMN ctpn3 TO third_contact_person_name")
    #     execute("ALTER TABLE vendors RENAME COLUMN ctph3 TO third_contact_person_phone")
    #     execute("ALTER TABLE vendors RENAME COLUMN ctem3 TO third_contact_person_email")

    #     execute("ALTER TABLE vendors RENAME COLUMN addr1 TO first_address")
    #     execute("ALTER TABLE vendors RENAME COLUMN city1 TO first_city")
    #     execute("ALTER TABLE vendors RENAME COLUMN prvc1 TO first_province")
    #     execute("ALTER TABLE vendors RENAME COLUMN cntr1 TO first_country")
    #     execute("ALTER TABLE vendors RENAME COLUMN pcod1 TO first_postal_code")
    #     execute("ALTER TABLE vendors RENAME COLUMN addr2 TO second_address")
    #     execute("ALTER TABLE vendors RENAME COLUMN city2 TO second_city")
    #     execute("ALTER TABLE vendors RENAME COLUMN prvc2 TO second_province")
    #     execute("ALTER TABLE vendors RENAME COLUMN cntr2 TO second_country")
    #     execute("ALTER TABLE vendors RENAME COLUMN pcod2 TO second_postal_code")
    #     execute("ALTER TABLE vendors RENAME COLUMN phone TO phone_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN faxno TO fax_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN webst TO website")

    #     execute("ALTER TABLE vendors RENAME COLUMN noemp TO employee_count")
    #     execute("ALTER TABLE vendors RENAME COLUMN nomgm TO management_count")
    #     execute("ALTER TABLE vendors RENAME COLUMN noadm TO administration_count")
    #     execute("ALTER TABLE vendors RENAME COLUMN notch TO technician_count")
    #     execute("ALTER TABLE vendors RENAME COLUMN nosls TO sales_count")
    #     execute("ALTER TABLE vendors RENAME COLUMN noqas TO quality_assurance_count")
    #     execute("ALTER TABLE vendors RENAME COLUMN noqcl TO quality_control_count")
    #     execute("ALTER TABLE vendors RENAME COLUMN nobrc TO branch_count")

    #     execute("ALTER TABLE vendors RENAME COLUMN sooff TO office_area")
    #     execute("ALTER TABLE vendors RENAME COLUMN ipoff TO office_area_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN sowhs TO warehouse_area")
    #     execute("ALTER TABLE vendors RENAME COLUMN ipwhs TO warehouse_area_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN somfr TO manufacture_area")
    #     execute("ALTER TABLE vendors RENAME COLUMN ipmfr TO manufacture_area_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN sooth TO others_area")
    #     execute("ALTER TABLE vendors RENAME COLUMN ipoth TO others_area_file")

    #     execute("ALTER TABLE vendors RENAME COLUMN curcd TO currency")
    #     execute("ALTER TABLE vendors RENAME COLUMN zbank TO bank_name")
    #     execute("ALTER TABLE vendors RENAME COLUMN bbank TO bank_branch")
    #     execute("ALTER TABLE vendors RENAME COLUMN cbank TO bank_city")
    #     execute("ALTER TABLE vendors RENAME COLUMN nbank TO bank_account_name")
    #     execute("ALTER TABLE vendors RENAME COLUMN rbank TO bank_account_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN incap TO authorized_capital")
    #     execute("ALTER TABLE vendors RENAME COLUMN finab TO financial_ability")
    #     execute("ALTER TABLE vendors RENAME COLUMN noast TO asset_count")
    #     execute("ALTER TABLE vendors RENAME COLUMN nniat TO niat")
    #     execute("ALTER TABLE vendors RENAME COLUMN ebitd TO ebitda")
    #     execute("ALTER TABLE vendors RENAME COLUMN annrv TO annual_revenue")
    #     execute("ALTER TABLE vendors RENAME COLUMN avarv TO average_revenue")

    #     execute("ALTER TABLE vendors RENAME COLUMN nnpwp TO npwp_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN inpwp TO npwp_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN njstk TO jamsostek_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN ijstk TO jamsostek_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN nakta TO business_establishment_deed_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN dakta TO business_establishment_deed_date")
    #     execute("ALTER TABLE vendors RENAME COLUMN iakta TO business_establishment_deed_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN nsiup TO siup_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN tsiup TO siup_type")
    #     execute("ALTER TABLE vendors RENAME COLUMN isiup TO siup_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN nbnib TO nib_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN expd1 TO nib_expiration_date")
    #     execute("ALTER TABLE vendors RENAME COLUMN ipnib TO nib_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN siujk TO siujk")
    #     execute("ALTER TABLE vendors RENAME COLUMN grde1 TO siujk_grade")
    #     execute("ALTER TABLE vendors RENAME COLUMN expd3 TO siujk_expiration_date")
    #     execute("ALTER TABLE vendors RENAME COLUMN isiuj TO siujk_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN sbujp TO sbujpk_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN grde2 TO sbujpk_grade")
    #     execute("ALTER TABLE vendors RENAME COLUMN expd4 TO sbujpk_expiration_date")
    #     execute("ALTER TABLE vendors RENAME COLUMN isbuj TO sbujk_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN nbiup TO iup_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN ipiup TO iup_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN nbsku TO sku_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN expd6 TO sku_expiration_date")
    #     execute("ALTER TABLE vendors RENAME COLUMN ipsku TO sku_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN nskdp TO skdp_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN expd2 TO skdp_expiration_date")
    #     execute("ALTER TABLE vendors RENAME COLUMN iskdp TO skdp_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN nsitu TO situ_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN expd5 TO situ_expiration_date")
    #     execute("ALTER TABLE vendors RENAME COLUMN isitu TO situ_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN sppkp TO sppkp_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN isppk TO sppkp_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN nbskt TO skt_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN ipskt TO skt_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN nbtdp TO tdp_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN iptdp TO tdp_file")

    #     execute("ALTER TABLE vendors RENAME COLUMN qfctn TO qualification")
    #     execute("ALTER TABLE vendors RENAME COLUMN refri TO referenced_by")
    #     execute("ALTER TABLE vendors RENAME COLUMN kadin TO kadin_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN ikdin TO kadin_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN sknkp TO sknkp_number")
    #     execute("ALTER TABLE vendors RENAME COLUMN iknkp TO sknkp_file")
    #     execute("ALTER TABLE vendors RENAME COLUMN otdoc TO other_document")
    #     execute("ALTER TABLE vendors RENAME COLUMN iotdc TO other_document_file")

    #     # execute("ALTER TABLE vendors RENAME COLUMN ippkp TO xxx")  # TODO
    #     # execute("ALTER TABLE vendors RENAME COLUMN ipctf TO xxx")  # TODO
    #     # execute("ALTER TABLE vendors RENAME COLUMN ipcpf TO xxx")  # TODO
    #     # execute("ALTER TABLE vendors RENAME COLUMN iporc TO xxx")  # TODO
    #     # execute("ALTER TABLE vendors RENAME COLUMN ipctr TO xxx")  # TODO
    #     # execute("ALTER TABLE vendors RENAME COLUMN ipjex TO xxx")  # TODO
    #     # execute("ALTER TABLE vendors RENAME COLUMN iplot TO xxx")  # TODO
    #     # execute("ALTER TABLE vendors RENAME COLUMN ipcsm TO xxx")  # TODO
    #     # execute("ALTER TABLE vendors RENAME COLUMN ippmt TO xxx")  # TODO

    #     # execute("ALTER TABLE vendors RENAME COLUMN regsn TO xxx")  # TODO
    #     print(":: BOOLEAN ::")
    #     # execute("ALTER TABLE vendors RENAME COLUMN compr TO xxx")  # TODO
    #     execute(
    #         """
    #         ALTER TABLE vendors
    #         ALTER COLUMN compr DROP DEFAULT,
    #         ALTER COLUMN compr TYPE BOOLEAN USING compr::INTEGER::BOOLEAN;
    #         """
    #     )
    #     execute(
    #         """
    #         ALTER TABLE vendors
    #         ALTER COLUMN compr SET DEFAULT TRUE;
    #         """
    #     )
    #     # execute("ALTER TABLE vendors RENAME COLUMN lglty TO xxx")  # TODO
    #     execute(
    #         """
    #         ALTER TABLE vendors
    #         ALTER COLUMN lglty DROP DEFAULT,
    #         ALTER COLUMN lglty TYPE BOOLEAN USING lglty::INTEGER::BOOLEAN;
    #         """
    #     )
    #     execute(
    #         """
    #         ALTER TABLE vendors
    #         ALTER COLUMN lglty SET DEFAULT TRUE;
    #         """
    #     )
    #     # execute("ALTER TABLE vendors RENAME COLUMN visit TO xxx")  # TODO
    #     execute(
    #         """
    #         ALTER TABLE vendors
    #         ALTER COLUMN visit DROP DEFAULT,
    #         ALTER COLUMN visit TYPE BOOLEAN USING visit::INTEGER::BOOLEAN;
    #         """
    #     )
    #     execute(
    #         """
    #         ALTER TABLE vendors
    #         ALTER COLUMN visit SET DEFAULT TRUE;
    #         """
    #     )
    #     execute("ALTER TABLE vendors RENAME COLUMN isagr TO is_agr")
    #     execute(
    #         """
    #         ALTER TABLE vendors
    #         ALTER COLUMN isagr DROP DEFAULT,
    #         ALTER COLUMN isagr TYPE BOOLEAN USING isagr::INTEGER::BOOLEAN;
    #         """
    #     )
    #     execute(
    #         """
    #         ALTER TABLE vendors
    #         ALTER COLUMN isagr SET DEFAULT TRUE;
    #         """
    #     )
    #     execute("ALTER TABLE vendors RENAME COLUMN isact TO is_active")
    #     execute(
    #         """
    #         ALTER TABLE vendors
    #         ALTER COLUMN is_active DROP DEFAULT,
    #         ALTER COLUMN is_active TYPE BOOLEAN USING is_active::INTEGER::BOOLEAN;
    #         """
    #     )
    #     execute(
    #         """
    #         ALTER TABLE vendors
    #         ALTER COLUMN is_active SET DEFAULT TRUE;
    #         """
    #     )
        # endregion: vendors
        # region: vendor_rfqs
        # execute("ALTER TABLE vendor_rfqs RENAME COLUMN trnno TO id")
        # execute("ALTER TABLE vendor_rfqs RENAME COLUMN fcoid TO branch_id")
        # execute("ALTER TABLE vendor_rfqs RENAME COLUMN vdrid TO vendor_id")
        # execute("ALTER TABLE vendor_rfqs RENAME COLUMN stats TO reference_id")
        # execute("ALTER TABLE vendor_rfqs RENAME COLUMN docno TO document_number")
        # execute("ALTER TABLE vendor_rfqs RENAME COLUMN trndt TO transaction_date")
        # execute("ALTER TABLE vendor_rfqs RENAME COLUMN fisyr TO year")
        # execute("ALTER TABLE vendor_rfqs RENAME COLUMN fismn TO month")
        # execute("ALTER TABLE vendor_rfqs RENAME COLUMN descr TO description")
        # execute("ALTER TABLE vendor_rfqs RENAME COLUMN appsc TO app_source")
        # execute("ALTER TABLE vendor_rfqs RENAME COLUMN sqenc TO sequence_number")
        # endregion: vendor_rfqs

        # region: rfqs
        # execute("ALTER TABLE rfqs RENAME COLUMN trnno TO id")
        # execute("""
        #     CREATE SEQUENCE rfqs_id_seq
        #     OWNED BY rfqs.id;

        #     ALTER TABLE rfqs
        #     ALTER COLUMN id SET DEFAULT nextval('rfqs_id_seq');
        # """)
        # execute("ALTER TABLE rfqs RENAME COLUMN fcoid TO branch_id")
        # execute("ALTER TABLE rfqs RENAME COLUMN vdrid TO vendor_id_list")
        # execute("ALTER TABLE rfqs RENAME COLUMN prcby TO procured_by")
        # execute("ALTER TABLE rfqs RENAME COLUMN stats TO reference_id")
        # execute("ALTER TABLE rfqs RENAME COLUMN trnty TO transaction_type")
        # execute("ALTER TABLE rfqs RENAME COLUMN docno TO document_number")
        # execute("ALTER TABLE rfqs RENAME COLUMN trndt TO transaction_date")
        # execute("ALTER TABLE rfqs RENAME COLUMN fisyr TO year")
        # execute("ALTER TABLE rfqs RENAME COLUMN fismn TO month")
        # execute("ALTER TABLE rfqs RENAME COLUMN descr TO description")
        # execute("ALTER TABLE rfqs RENAME COLUMN appsc TO app_source")
        # execute("ALTER TABLE rfqs RENAME COLUMN sqenc TO sequence_number")


        # region: rfq_items
        # execute("ALTER TABLE rfq_items RENAME COLUMN trnno TO rfq_id;")
        # execute("ALTER TABLE rfq_items RENAME COLUMN lnnum TO line_number;")
        # execute("ALTER TABLE rfq_items RENAME COLUMN prtno TO procurement_request_id;")
        # execute("ALTER TABLE rfq_items RENAME COLUMN itmcd TO item_id;")
        # execute("ALTER TABLE rfq_items DROP COLUMN itmcd;")
        # execute("ALTER TABLE rfq_items DROP COLUMN prqty;")
        # execute("ALTER TABLE rfq_items DROP COLUMN unoms;")
        # execute("ALTER TABLE rfq_items DROP COLUMN curcd;")
        # # execute("ALTER TABLE rfq_items RENAME COLUMN bgprc TO ;")
        # execute("ALTER TABLE rfq_items DROP COLUMN descr;")
        # execute("ALTER TABLE rfq_items DROP COLUMN prnum;")
        # endregion: rfq_items
        # endregion: rfqs

        # endregion: group: vendors


        # region: group: assessments
        # region: vendor_assessments
        # execute("ALTER TABLE vendor_assessments RENAME COLUMN apvno TO id")
        # execute("ALTER TABLE vendor_assessments RENAME COLUMN vdrid TO vendor_id")
        # execute("ALTER TABLE vendor_assessments RENAME COLUMN apvun TO assessor_user_id")
        # execute("ALTER TABLE vendor_assessments RENAME COLUMN stats TO reference_id")
        # execute("ALTER TABLE vendor_assessments DROP COLUMN created_at")
        # execute("ALTER TABLE vendor_assessments RENAME COLUMN apvdt TO created_at")
        # execute("ALTER TABLE vendor_assessments RENAME COLUMN apvnt TO assessment_notes")
        # endregion: vendor_assessments

        # region: procurement_request_assessments
        # execute("ALTER TABLE procurement_request_assessments RENAME COLUMN apvno TO id;")
        # execute("ALTER TABLE procurement_request_assessments RENAME COLUMN trnno TO procurement_request_id;")
        # execute("ALTER TABLE procurement_request_assessments RENAME COLUMN stats TO reference_id;")
        # execute("ALTER TABLE procurement_request_assessments RENAME COLUMN apvnt TO assessment_notes;")
        # execute("ALTER TABLE procurement_request_assessments RENAME COLUMN apvun TO assessor_user_id;")
        # execute("ALTER TABLE procurement_request_assessments DROP COLUMN created_at;")
        # execute("ALTER TABLE procurement_request_assessments RENAME COLUMN apvdt TO created_at;")
        # endregion: procurement_request_assessments
        # endregion: group: assessments



        # region: procurement_requests
        # execute("ALTER TABLE procurement_requests RENAME COLUMN trnno TO id")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN brcid TO branch_id")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN dirid TO directorate_id")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN divid TO division_id")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN depid TO department_id")
        # execute("ALTER TABLE procurement_requests DROP COLUMN dapid;")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN coacd TO cost_center_id")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN catcd TO item_class_id;")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN grpcd TO item_category_id;")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN entby TO preparer_id")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN reqby TO requester_id")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN stats TO reference_id")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN trndt TO transaction_date")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN trnty TO transaction_type")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN fisyr TO year")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN fismn TO month")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN descr TO description")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN docno TO document_number")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN appsc TO app_source")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN sqenc TO sequence_number")
        # execute("ALTER TABLE procurement_requests RENAME COLUMN isugn TO is_ugn")
        # execute(
        #     """
        #     ALTER TABLE procurement_requests
        #     ALTER COLUMN is_ugn TYPE BOOLEAN USING is_ugn::INTEGER::BOOLEAN;
        #     """
        # )
        # execute("ALTER TABLE procurement_requests ALTER COLUMN is_ugn SET DEFAULT FALSE;")

        # execute("""
        #     CREATE SEQUENCE procurement_requests_id_seq
        #     OWNED BY procurement_requests.id;

        #     ALTER TABLE procurement_requests
        #     ALTER COLUMN id SET DEFAULT nextval('procurement_requests_id_seq');
        # """)

        # execute("""
        #     ALTER TABLE procurement_requests
        #     ALTER COLUMN description DROP DEFAULT,
        #     ALTER COLUMN description DROP NOT NULL;
        # """)
        # endregion: procurement_requests

        # region: group: purchase_orders
        # region: purchase_orders
        # execute("ALTER TABLE purchase_orders RENAME COLUMN trnno TO id")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN fcoid TO branch_id")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN descr TO description;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN isact TO is_active;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN vdrid TO vendor_id;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN stats TO reference_id;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN trnty TO transaction_type;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN trndt TO transaction_date;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN docno TO document_number;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN potyp TO purchase_order_type;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN curcd TO currency;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN appsc TO app_source;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN sqenc TO sequence_number;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN paytm TO payment_time;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN paypd TO payment_period;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN paynt TO payment_note;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN discn TO discount;")
        # execute("ALTER TABLE purchase_orders RENAME COLUMN pcppn TO tax_percentage;")
        # endregion: purchase_orders

        # region: purchase_order_items
        # execute("ALTER TABLE purchase_order_items ALTER COLUMN lnrf1 DROP DEFAULT;")
        # execute("ALTER TABLE purchase_order_items ALTER COLUMN lnrf2 DROP DEFAULT;")
        # execute("ALTER TABLE purchase_order_items ALTER COLUMN lnrf3 DROP DEFAULT;")

        # execute("ALTER TABLE purchase_order_items RENAME COLUMN trnno TO purchase_order_id;")
        # execute("ALTER TABLE purchase_order_items RENAME COLUMN lnnum TO line_number;")
        # execute("ALTER TABLE purchase_order_items RENAME COLUMN itmcd TO item_id;")
        # execute("ALTER TABLE purchase_order_items RENAME COLUMN itmqt TO item_quantity;")
        # execute("ALTER TABLE purchase_order_items RENAME COLUMN amont TO amount;")
        # execute("ALTER TABLE purchase_order_items RENAME COLUMN dcamt TO discount_amount;")
        # execute("ALTER TABLE purchase_order_items RENAME COLUMN pnamt TO tax_amount;")
        # execute("ALTER TABLE purchase_order_items RENAME COLUMN ntamt TO net_amount;")
        # execute("ALTER TABLE purchase_order_items RENAME COLUMN netpc TO net_price;")
        # execute("ALTER TABLE purchase_order_items RENAME COLUMN reqdt TO required_date;")
        # # execute("ALTER TABLE purchase_order_items RENAME COLUMN lnrf1 TO ;")
        # # execute("ALTER TABLE purchase_order_items RENAME COLUMN lnrf2 TO ;")
        # # execute("ALTER TABLE purchase_order_items RENAME COLUMN lnrf3 TO ;")
        # # execute("ALTER TABLE purchase_order_items RENAME COLUMN lnri1 TO ;")
        # # execute("ALTER TABLE purchase_order_items RENAME COLUMN lnri2 TO ;")
        # # execute("ALTER TABLE purchase_order_items RENAME COLUMN lnri3 TO ;")
        # # execute("ALTER TABLE purchase_order_items RENAME COLUMN lnrd1 TO ;")
        # # execute("ALTER TABLE purchase_order_items RENAME COLUMN lnrd2 TO ;")
        # # execute("ALTER TABLE purchase_order_items RENAME COLUMN lnrd3 TO ;")
        # endregion: purchase_order_items
        # endregion: group: purchase_orders

        # region: price_comparisons
        # execute("ALTER TABLE price_comparisons RENAME COLUMN trnno TO id")
        # execute("ALTER TABLE price_comparisons RENAME COLUMN rfqtn TO rfq_id")
        # execute("ALTER TABLE price_comparisons RENAME COLUMN stats TO reference_id")
        # execute("ALTER TABLE price_comparisons RENAME COLUMN docno TO document_number")
        # execute("ALTER TABLE price_comparisons RENAME COLUMN trndt TO transaction_date")
        # execute("ALTER TABLE price_comparisons RENAME COLUMN trnty TO transaction_type")
        # execute("ALTER TABLE price_comparisons RENAME COLUMN fisyr TO year")
        # execute("ALTER TABLE price_comparisons RENAME COLUMN fismn TO month")
        # execute("ALTER TABLE price_comparisons RENAME COLUMN descr TO description")
        # execute("ALTER TABLE price_comparisons RENAME COLUMN appsc TO app_source")
        # execute("ALTER TABLE price_comparisons RENAME COLUMN sqenc TO sequence_number")
        # endregion: price_comparisons

        # region: budgets
        # execute("ALTER TABLE budgets RENAME COLUMN coacd to cost_center_id;")
        # execute("ALTER TABLE budgets RENAME COLUMN budyr to year;")
        # execute("ALTER TABLE budgets RENAME COLUMN upnum to upload_count;")
        # execute("ALTER TABLE budgets RENAME COLUMN budvl to amount;")

        # execute("ALTER TABLE budgets DROP COLUMN temps;")
        # endregion: budgets

        # region: cost_centers
        # execute(
        #     """
        #     ALTER TABLE cost_centers
        #     ALTER COLUMN alldb DROP DEFAULT,
        #     ALTER COLUMN alldb TYPE BOOLEAN USING alldb::INTEGER::BOOLEAN;
        #     """
        # )
        # execute("ALTER TABLE cost_centers ALTER COLUMN alldb SET DEFAULT TRUE;")
        # execute(
        #     """
        #     ALTER TABLE cost_centers
        #     ALTER COLUMN allcr DROP DEFAULT,
        #     ALTER COLUMN allcr TYPE BOOLEAN USING allcr::INTEGER::BOOLEAN;
        #     """
        # )
        # execute("ALTER TABLE cost_centers ALTER COLUMN allcr SET DEFAULT TRUE;")
        # execute(
        #     """
        #     ALTER TABLE cost_centers
        #     ALTER COLUMN isfxd DROP DEFAULT,
        #     ALTER COLUMN isfxd TYPE BOOLEAN USING isfxd::INTEGER::BOOLEAN;
        #     """
        # )

        # execute("ALTER TABLE cost_centers RENAME COLUMN isact to is_active;")
        # execute(
        #     """
        #     ALTER TABLE cost_centers
        #     ALTER COLUMN is_active DROP DEFAULT,
        #     ALTER COLUMN is_active TYPE BOOLEAN USING is_active::INTEGER::BOOLEAN;
        #     """
        # )
        # execute("ALTER TABLE cost_centers ALTER COLUMN is_active SET DEFAULT TRUE;")
        # execute("ALTER TABLE cost_centers RENAME COLUMN coacd to id;")
        # execute("ALTER TABLE cost_centers RENAME COLUMN descr to description;")
        # # execute("ALTER TABLE cost_centers RENAME COLUMN coafc to ;")
        # # execute("ALTER TABLE cost_centers RENAME COLUMN coagp to ;")
        # drop_default_if_exists(["cost_centers"], "coagp")
        # drop_default_if_exists(["cost_centers"], "description")
        # execute("""
        #     ALTER TABLE cost_centers
        #     ALTER COLUMN rqsub DROP DEFAULT,
        #     ALTER COLUMN rqsub DROP NOT NULL;
        # """)
        # # execute("ALTER TABLE cost_centers RENAME COLUMN rqsub to ;")
        # execute("ALTER TABLE cost_centers ALTER COLUMN rqprc SET DEFAULT 0;")
        # # execute("ALTER TABLE cost_centers RENAME COLUMN rqprc to ;")
        # # execute("ALTER TABLE cost_centers RENAME COLUMN rqatt to ;")
        # endregion: cost_centers


        # region: inventories
        # execute("ALTER TABLE inventories RENAME COLUMN trnno TO id")
        # execute("ALTER TABLE inventories RENAME COLUMN brcid TO branch_id")
        # execute("ALTER TABLE inventories RENAME COLUMN vdrid TO vendor_id")
        # execute("ALTER TABLE inventories RENAME COLUMN wshid TO warehouse_id")
        # execute("ALTER TABLE inventories RENAME COLUMN trndt TO transaction_date")
        # execute("ALTER TABLE inventories RENAME COLUMN fisyr TO year")
        # execute("ALTER TABLE inventories RENAME COLUMN fismn TO month")
        # execute("ALTER TABLE inventories RENAME COLUMN trnty TO transaction_type")
        # execute("ALTER TABLE inventories RENAME COLUMN docno TO document_number")
        # execute("ALTER TABLE inventories RENAME COLUMN descr TO description")

        # TODO
        ...
        # endregion: inventories


        # region: group: items
        # region: items
        # execute("ALTER TABLE items RENAME COLUMN itmcd TO id;")
        # execute("ALTER TABLE items RENAME COLUMN grpcd TO item_category_id;")
        # execute("ALTER TABLE items RENAME COLUMN coacd TO cost_center_id;")
        # execute("ALTER TABLE items RENAME COLUMN descr TO description;")
        # execute("ALTER TABLE items RENAME COLUMN unoms TO unit_of_measurement;")
        # execute("ALTER TABLE items RENAME COLUMN minqt TO minimum_quantity;")
        # execute("ALTER TABLE items RENAME COLUMN slavl TO sla;")
        # execute(
        #     """
        #     ALTER TABLE items
        #     ALTER COLUMN isadj DROP DEFAULT,
        #     ALTER COLUMN isadj TYPE BOOLEAN USING isadj::INTEGER::BOOLEAN;

        #     ALTER TABLE items
        #     ALTER COLUMN isadj SET DEFAULT FALSE;
        #     """
        # )
        # execute("ALTER TABLE items RENAME COLUMN isadj TO is_adjustable;")
        # execute("ALTER TABLE items RENAME COLUMN isact TO is_active;")
        # execute(
        #     """
        #     ALTER TABLE items
        #     ALTER COLUMN is_active DROP DEFAULT,
        #     ALTER COLUMN is_active TYPE BOOLEAN USING is_active::INTEGER::BOOLEAN;

        #     ALTER TABLE items
        #     ALTER COLUMN is_active SET DEFAULT TRUE;
        #     """
        # )
        # execute("ALTER TABLE items RENAME COLUMN otags TO tags;")

        # execute("ALTER TABLE items ALTER COLUMN description DROP DEFAULT;")
        # execute("ALTER TABLE items ALTER COLUMN unit_of_measurement DROP DEFAULT;")
        # execute("ALTER TABLE items ALTER COLUMN cost_center_id DROP DEFAULT;")
        # execute("ALTER TABLE items ALTER COLUMN item_group_id DROP DEFAULT;")
        # endregion: items

        # region: item_classes
        # execute("ALTER TABLE item_classes RENAME COLUMN catcd TO id;")
        # execute("ALTER TABLE item_classes RENAME COLUMN descr TO description;")
        # execute("ALTER TABLE item_classes RENAME COLUMN isact TO is_active;")
        # execute(
        #     """
        #     ALTER TABLE item_classes
        #     ALTER COLUMN is_active DROP DEFAULT,
        #     ALTER COLUMN is_active TYPE BOOLEAN USING is_active::INTEGER::BOOLEAN;

        #     ALTER TABLE item_classes
        #     ALTER COLUMN is_active SET DEFAULT TRUE;
        #     """
        # )
        # endregion: item_classes

        # region: item_categories
        # execute("ALTER TABLE item_categories RENAME COLUMN grpcd TO id;")
        # execute("ALTER TABLE item_categories RENAME COLUMN catcd TO item_class_id;")
        # execute("ALTER TABLE item_categories RENAME COLUMN coacd TO cost_center_id;")
        # execute("ALTER TABLE item_categories RENAME COLUMN descr TO description;")
        # execute("ALTER TABLE item_categories RENAME COLUMN isact TO is_active;")
        # execute(
        #     """
        #     ALTER TABLE item_categories
        #     ALTER COLUMN is_active DROP DEFAULT,
        #     ALTER COLUMN is_active TYPE BOOLEAN USING is_active::INTEGER::BOOLEAN;

        #     ALTER TABLE item_categories
        #     ALTER COLUMN is_active SET DEFAULT TRUE;
        #     """
        # )
        # # execute("ALTER TABLE item_categories RENAME COLUMN fanfa TO ;")  # TODO
        # # execute("ALTER TABLE item_categories RENAME COLUMN pcsfl TO ;")
        # # execute("ALTER TABLE item_categories RENAME COLUMN pcsun TO ;")
        # # execute("ALTER TABLE item_categories RENAME COLUMN pcsby TO ;")
        # # execute("ALTER TABLE item_categories RENAME COLUMN apvl1 TO ;")
        # # execute("ALTER TABLE item_categories RENAME COLUMN apvl2 TO ;")
        # # execute("ALTER TABLE item_categories RENAME COLUMN pcsem TO ;")
        # # execute("ALTER TABLE item_categories RENAME COLUMN coadp TO ;")
        # # execute("ALTER TABLE item_categories RENAME COLUMN coatr TO ;")
        # execute(
        #     """
        #     ALTER TABLE item_categories
        #     ALTER COLUMN slavl DROP DEFAULT,
        #     ALTER COLUMN slavl TYPE BOOLEAN USING slavl::INTEGER::BOOLEAN;

        #     ALTER TABLE item_categories
        #     ALTER COLUMN slavl SET DEFAULT TRUE;
        #     """
        # )
        # execute("ALTER TABLE item_categories RENAME COLUMN slavl TO sla;")
        # endregion: item_categories


        # region: procurement_request_items
        # execute("ALTER TABLE procurement_request_items RENAME COLUMN trnno to procurement_request_id;")
        # execute("ALTER TABLE procurement_request_items RENAME COLUMN lnnum to line_number;")
        # execute("ALTER TABLE procurement_request_items RENAME COLUMN itmcd to item_id;")
        # execute("ALTER TABLE procurement_request_items RENAME COLUMN curcd TO currency_id;")
        # execute("ALTER TABLE procurement_request_items RENAME COLUMN itmqt TO quantity;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN aprqt TO ;")
        # execute("ALTER TABLE procurement_request_items RENAME COLUMN unoms TO unit_of_measurement;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN esprc TO ;")
        # execute("ALTER TABLE procurement_request_items RENAME COLUMN reqit TO required_days_interval;")
        # execute("ALTER TABLE procurement_request_items RENAME COLUMN reqdt TO required_date;")
        # execute("ALTER TABLE procurement_request_items RENAME COLUMN itmds TO notes;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN ktuck TO ;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN gmkck TO ;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN uhock TO ;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN ghock TO ;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN budck TO ;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN bcchk TO ;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN mdchk TO ;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN rdcrt TO ;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN odrop TO ;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN aloct TO ;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN ipath TO ;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN pictr TO ;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN picty TO ;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN picfn TO ;")
        # # execute("ALTER TABLE procurement_request_items RENAME COLUMN picsz TO ;")
        # TODO
        # ...
        # endregion: procurement_request_items

        # endregion: group: items




        # region: group: invoices

        # region: invoices
        # execute("ALTER TABLE invoices RENAME COLUMN trnno TO id;")
        # execute("ALTER TABLE invoices RENAME COLUMN trndt TO transaction_date;")
        # execute("ALTER TABLE invoices RENAME COLUMN fisyr TO year;")
        # execute("ALTER TABLE invoices RENAME COLUMN fismn TO month;")
        # execute("ALTER TABLE invoices RENAME COLUMN vdrid TO vendor_id;")
        # execute("ALTER TABLE invoices RENAME COLUMN invdt TO invoice_date;")
        # execute("ALTER TABLE invoices RENAME COLUMN invno TO invoice_number;")
        # execute("ALTER TABLE invoices RENAME COLUMN invvl TO invoice_amount;")
        # execute("ALTER TABLE invoices RENAME COLUMN trmin TO termin;")
        # execute("ALTER TABLE invoices RENAME COLUMN potno TO purchase_order_id;")
        # execute("ALTER TABLE invoices RENAME COLUMN sqenc TO sequence_number;")
        # execute("ALTER TABLE invoices RENAME COLUMN docno TO document_number;")
        # execute("ALTER TABLE invoices RENAME COLUMN stats TO reference_id;")
        # execute("ALTER TABLE invoices RENAME COLUMN appsc TO app_source;")
        # execute("ALTER TABLE invoices RENAME COLUMN descr TO description;")
        # execute("ALTER TABLE invoices RENAME COLUMN ipath TO image_path;")
        # execute("ALTER TABLE invoices RENAME COLUMN crgto TO cost_center_id;")
        # execute("ALTER TABLE invoices RENAME COLUMN invpn TO tax_percentage;")

        # execute("ALTER TABLE invoices ALTER COLUMN invoice_number DROP DEFAULT;")
        # execute("ALTER TABLE invoices ALTER COLUMN document_number DROP DEFAULT;")

        # execute("""
        #     CREATE SEQUENCE invoice_id_seq
        #     OWNED BY invoices.id;

        #     ALTER TABLE invoices
        #     ALTER COLUMN id SET DEFAULT nextval('invoice_id_seq');
        # """)

        # execute("""
        #     ALTER TABLE invoices
        #     ALTER COLUMN description DROP DEFAULT,
        #     ALTER COLUMN description DROP NOT NULL;
        # """)
        # endregion: invoices

        # region: invoice_assessments
        # execute("ALTER TABLE invoice_assessments RENAME COLUMN apvno TO id;")
        # execute("ALTER TABLE invoice_assessments RENAME COLUMN trnno TO procurement_request_id;")
        # execute("ALTER TABLE invoice_assessments RENAME COLUMN stats TO reference_id;")
        # execute("ALTER TABLE invoice_assessments RENAME COLUMN apvnt TO assessment_notes;")
        # execute("ALTER TABLE invoice_assessments RENAME COLUMN apvun TO assessor_user_id;")
        # execute("ALTER TABLE invoice_assessments DROP COLUMN created_at;")
        # execute("ALTER TABLE invoice_assessments RENAME COLUMN apvdt TO created_at;")
        # endregion: invoice_assessments

        # endregion: group: invoices




        # region: group: petty_cash_claims
        # region: petty_cash_claims
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN trnno TO id")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN brcid TO branch_id")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN trndt TO transaction_date")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN fisyr TO `year`")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN fismn TO `month`")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN catcd TO item_class_id")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN grpcd TO item_category_id")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN sqenc TO sequence_number")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN docno TO document_number")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN coacd TO cost_center_id")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN descr TO description")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN reqdt TO required_date")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN reqby TO requester_id")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN entby TO preparer_id")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN stats TO reference_id")
        # execute("ALTER TABLE petty_cash_claims RENAME COLUMN appsc TO app_source")
        # endregion: petty_cash_claims

        # region: petty_cash_claim_assessments
        # execute("ALTER TABLE petty_cash_claim_assessments RENAME COLUMN apvno TO id;")
        # execute("ALTER TABLE petty_cash_claim_assessments RENAME COLUMN trnno TO procurement_request_id;")
        # execute("ALTER TABLE petty_cash_claim_assessments RENAME COLUMN stats TO reference_id;")
        # execute("ALTER TABLE petty_cash_claim_assessments RENAME COLUMN apvnt TO assessment_notes;")
        # execute("ALTER TABLE petty_cash_claim_assessments RENAME COLUMN apvun TO assessor_user_id;")
        # execute("ALTER TABLE petty_cash_claim_assessments DROP COLUMN created_at;")
        # execute("ALTER TABLE petty_cash_claim_assessments RENAME COLUMN apvdt TO created_at;")
        # endregion: petty_cash_claim_assessments
        # endregion: group: petty_cash_claims




        # region: links
        # execute("ALTER TABLE links RENAME COLUMN lnkid TO id;")
        # execute("ALTER TABLE links RENAME COLUMN lnktx TO url;")
        # execute("ALTER TABLE links RENAME COLUMN descr TO description;")
        # execute("ALTER TABLE links RENAME COLUMN modul TO module;")
        # execute("ALTER TABLE links RENAME COLUMN usrid TO user_id;")
        # execute("ALTER TABLE links RENAME COLUMN paswd TO password;")
        # execute("ALTER TABLE links RENAME COLUMN mailt TO mail_to;")
        # execute("ALTER TABLE links RENAME COLUMN mailc TO mail_cc;")
        # execute("ALTER TABLE links RENAME COLUMN mails TO mail_subject;")
        # execute("ALTER TABLE links RENAME COLUMN mailm TO mail_content;")
        # execute("ALTER TABLE links RENAME COLUMN mailf TO mail_attachment;")
        # # execute("ALTER TABLE links RENAME COLUMN refid TO ;")
        # endregion: links



        # region: activity_logs        
        # execute("ALTER TABLE activity_logs RENAME COLUMN logid TO id;")
        # execute("ALTER TABLE activity_logs RENAME COLUMN actvt TO activity;")
        # endregion: activity_logs



        # NOTE: NEW TABLE ! ! !
        # execute("""
        #     CREATE TABLE user_tokens (
        #         id BIGSERIAL PRIMARY KEY,
        #         auth_token VARCHAR(255) NOT NULL,
        #         user_id VARCHAR(24) NOT NULL,
        #         expires_at TIMESTAMP NOT NULL,
        #         is_active BOOLEAN DEFAULT TRUE,
        #         created_at TIMESTAMP DEFAULT NOW(),
        #         updated_at TIMESTAMP DEFAULT NOW(),
        #         updated_by VARCHAR(24),
        #         is_deleted BOOLEAN DEFAULT FALSE,
        #         deleted_at TIMESTAMP
        #     );
        # """)

    except:
        pass

    conn.close()
    cursor.close()
