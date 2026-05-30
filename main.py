
from affective import (
    run,
    handle,
    Continuation,
    RunningContinuation,
    catch,
    Affects,
)
from affective.std.stdio import default_stdio_handler, Console
from sample_app.app.effects import UserStorage

from sample_app.app.usecase import register_user
from sample_app.handlers.user_mgmt import test_user_mgmt_handler


def ask_for_name() -> Affects[str, Console]:
    yield from Console.write("What is your name? ")
    name = yield from Console.read()
    return name


def main() -> Affects[None, Console | UserStorage]:
    name = yield from ask_for_name()

    @catch
    def catch_error(_: Continuation[...], err: Exception) -> RunningContinuation:
        yield from Console.write(f"Error! {err!r}, aborting.")

    yield from handle(catch_error, register_user(name))


if __name__ == "__main__":
    run(
        handle(
            default_stdio_handler + test_user_mgmt_handler,
            main(),
        )
    )
