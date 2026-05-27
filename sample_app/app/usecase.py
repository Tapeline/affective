from affective import Raise
from sample_app.app.domain import User
from sample_app.app.effects import SaveUser, ReadUser


class UserAlreadyExists(Exception):
    ...


def register_user(name: str):
    existing = yield ReadUser(name)
    if existing:
        yield Raise(UserAlreadyExists())
    user = User(name)
    yield SaveUser(user)
