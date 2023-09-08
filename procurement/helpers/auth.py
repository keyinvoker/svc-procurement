from procurement.models.users.admins import Admin


def get_salt_from_database(email: str) -> str:

    admin: Admin = (
        Admin.query
        .filter(Admin.email == email)
        .first()
    )

    return admin.salt
