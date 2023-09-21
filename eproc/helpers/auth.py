from eproc.models.users.users import User


def get_salt_from_database(email: str) -> str:

    admin: User = (
        User.query
        .filter(User.email == email)
        .first()
    )

    return admin.salt
