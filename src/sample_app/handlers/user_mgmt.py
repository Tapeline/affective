from typing import Any

from affective import Continuation, RunningContinuation, handler, Affects
from affective.std.stdio import Console

from sample_app.app.domain import User
from sample_app.app.effects import UserStorage


@handler(UserStorage.save_user)
def test_user_saver(
    then: Continuation[[None]], user: User
) -> Affects[Any, Console]:
    yield from Console.write(f"User {user.name} saved\n")
    ret = yield from then(None)
    return ret


@handler(UserStorage.read_user)
def test_user_reader(
    then: Continuation[[User | None]], name: str
) -> Affects[Any, Console]:
    yield from Console.write(f"Does user {name} exist? (y/N)")
    does_exist = yield from Console.read()
    if does_exist == "y":
        user = User(name)
    else:
        user = None
    ret = yield from then(user)
    return ret


test_user_mgmt_handler = test_user_reader + test_user_saver
