from collections.abc import Callable

from affective.std.stdio import WriteStdin, ReadStdin
from sample_app.app.domain import User
from sample_app.app.effects import SaveUser, ReadUser
from affective import Continuation, Handler


def test_user_saver(
    eff: SaveUser, then: Callable[[None], Continuation]
) -> Continuation:
    yield WriteStdin(f"User {eff.user.name} saved")
    ret = yield from then(None)
    return ret


def test_user_reader(
    eff: ReadUser, then: Callable[[User | None], Continuation]
) -> Continuation:
    yield WriteStdin(f"Does user {eff.name} exist? (y/N)")
    does_exist = yield ReadStdin()
    if does_exist:
        user = User(eff.name)
    else:
        user = None
    ret = yield from then(user)
    return ret


test_user_mgmt_handler = Handler(test_user_saver, test_user_reader)
