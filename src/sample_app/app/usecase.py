from affective import Raise, Affects
from affective.std.http import Http

from sample_app.app.domain import User
from sample_app.app.effects import MemeFetcher, UserStorage


class UserAlreadyExists(Exception):
    ...


def register_user(name: str) -> Affects[
    str, UserStorage | MemeFetcher | Raise[UserAlreadyExists]
]:
    existing = yield from UserStorage.read_user(name)
    if existing:
        yield from Raise.error(UserAlreadyExists())
    user = User(name)
    yield from UserStorage.save_user(user)
    user_joke = yield from MemeFetcher.get_joke()
    return user_joke
