from collections.abc import Callable

from affective.std.stdio import Console
from sample_app.app.domain import User
from sample_app.app.effects import UserStorage
from affective import Continuation, handler


@handler(UserStorage.save_user)
def test_user_saver(
    then: Callable[[None], Continuation], user: User
) -> Continuation:
    yield from Console.write(f"User {user.name} saved")
    ret = yield from then(None)
    return ret


@handler(UserStorage.read_user)
def test_user_reader(
    then: Callable[[User | None], Continuation], name: str
) -> Continuation:
    yield from Console.write(f"Does user {name} exist? (y/N)")
    does_exist = yield from Console.read()
    if does_exist == "y":
        user = User(name)
    else:
        user = None
    ret = yield from then(user)
    return ret


test_user_mgmt_handler = test_user_reader + test_user_saver

