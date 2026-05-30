from affective import Raise, Affects

from sample_app.app.domain import User
from sample_app.app.effects import UserStorage


class UserAlreadyExists(Exception):
    ...


def register_user(name: str) -> Affects[
    None, UserStorage | Raise[UserAlreadyExists]
]:
    existing = yield from UserStorage.read_user(name)
    if existing:
        yield from Raise.error(UserAlreadyExists())
    user = User(name)
    yield from UserStorage.save_user(user)
