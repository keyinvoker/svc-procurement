import psycopg2

from constants import to_be_renamed_tables


to_be_removed_tables = [
    "qurolor", "qugrpor_old", "ztlap_old"
]


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


if __name__ == "__main__":
    status, conn, cursor = get_connection_and_cursor()

    if status:
        # region NOTE: change old name to new name tables
        for old_name, new_name in to_be_renamed_tables.items():
            if not new_name:
                continue

            query = f"ALTER TABLE \"{old_name}\" RENAME TO \"{new_name}\""

            try:
                cursor.execute(query)
                conn.commit()
                print(f"Renamed :: {old_name} to {new_name}")
            except Exception as e:
                conn.rollback()
                continue
        # endregion


        # region: DROP (one-time)
        # for table in to_be_removed_tables:
        #     query = f"DROP TABLE {table}"

        #     try:
        #         cursor.execute(query)
        #         conn.commit()
        #         print(f"Successful :: dropped {table}")
        #     except Exception as e:
        #         conn.rollback()
                # print(f"Error :: {e}")
        #         continue
        # endregion


        # region NOTE: change field names: `ludat` -> `updated_at`, `lunam` -> `updated_by`
        # for old_name, new_name in to_be_renamed_tables.items():
        #     name = new_name if new_name else old_name

        #     try:
        #         cursor.execute(f"SELECT updated_at FROM {name}")
        #     except:
        #         conn.rollback()
        #         try:
        #             query = f"ALTER TABLE \"{name}\" RENAME COLUMN ludat TO updated_at;"
        #             cursor.execute(query)
        #             conn.commit()
        #             print(f"Successful :: unabbreviated on: {name}")
        #         except:
        #             conn.rollback()
        #             base_query = f"ALTER TABLE \"{name}\" ADD COLUMN"
        #             try:
        #                 query = f"{base_query} updated_at TIMESTAMP DEFAULT NULL;"
        #                 cursor.execute(query)
        #                 conn.commit()
        #             except:
        #                 conn.rollback()

        #     try:
        #         cursor.execute(f"SELECT updated_by FROM {name}")
        #     except:
        #         conn.rollback()
        #         try:
        #             query = f"ALTER TABLE \"{name}\" RENAME COLUMN lunam TO updated_by;"
        #             cursor.execute(query)
        #             conn.commit()
        #             print(f"Successful :: unabbreviated on: {name}")
        #         except:
        #             conn.rollback()
        #             base_query = f"ALTER TABLE \"{name}\" ADD COLUMN"
        #             try:
        #                 query = f"{base_query} updated_by VARCHAR DEFAULT NULL;"
        #                 cursor.execute(query)
        #                 conn.commit()
        #             except:
        #                 conn.rollback()
        # endregion


        # region NOTE: Insert `created_at`, `is_deleted`, `deleted_at`
        # for old_name, new_name in to_be_renamed_tables.items():
        #     name = new_name if new_name else old_name

        #     base_query = f"ALTER TABLE \"{name}\" ADD COLUMN"

        #     try:
        #         query = f"{base_query} created_at TIMESTAMP DEFAULT NULL;"
        #         cursor.execute(query)
        #         conn.commit()
        #         print(f"Successful :: altered table (created_at): {name}")
        #     except Exception as e:
        #         conn.rollback()
        #     try:
        #         query = f"UPDATE \"{name}\" SET created_at = updated_at WHERE created_at IS NULL;"
        #         cursor.execute(query)
        #         conn.commit()
        #         print(f"Successful :: altered table (created_at values): {name}")
        #     except Exception as e:
        #         conn.rollback()
        #     try:
        #         query = f"{base_query} is_deleted BOOLEAN NOT NULL DEFAULT FALSE;"
        #         cursor.execute(query)
        #         conn.commit()
        #         print(f"Successful :: altered table (is_deleted): {name}")
        #     except Exception as e:
        #         conn.rollback()
        #     try:
        #         query = f"{base_query} deleted_at TIMESTAMP DEFAULT NULL;"
        #         cursor.execute(query)
        #         conn.commit()
        #         print(f"Successful :: altered table (deleted_at): {name}")
        #     except Exception as e:
        #         conn.rollback()
        # endregion








        # try:
        #     name = "vendors"

        #     base_query = f"ALTER TABLE \"{name}\" ADD COLUMN"
        #     query = f"{base_query} created_at TIMESTAMP DEFAULT NULL;"
        #     query += f"UPDATE \"{name}\" SET created_at = updated_at WHERE created_at IS NULL;"
        #     query = f"{base_query} is_deleted BOOLEAN NOT NULL DEFAULT FALSE;"
        #     query += f"{base_query} deleted_at TIMESTAMP DEFAULT NULL;"

        #     cursor.execute(query)
        #     conn.commit()
        #     print(f"Successful :: altered table: {name}")
        # except Exception as e:
        #     print(f"Error :: {e}")




        conn.close()
        cursor.close()
