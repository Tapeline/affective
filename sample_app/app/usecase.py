from sample_app.app.domain import User
from sample_app.app.effects import SaveUser, ReadUser


class UserAlreadyExists(Exception):
    ...


def register_user(name: str):
    existing = yield ReadUser(name)
    if existing:
        raise UserAlreadyExists()
    user = User(name)
    yield SaveUser(user)
