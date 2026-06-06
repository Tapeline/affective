import asyncio

from affective import (
    handle,
    Continuation,
    catch,
    Affects,
)
from affective.core.loop import arun
from affective.std.http import async_http_handler
from affective.std.stdio import default_stdio_handler, Console
from sample_app.app.effects import UserStorage

from sample_app.app.usecase import register_user
from sample_app.handlers.joke_api import handle_get_joke
from sample_app.handlers.user_mgmt import test_user_mgmt_handler


def ask_for_name() -> Affects[str, Console]:
    yield from Console.write("What is your name? ")
    name = yield from Console.read()
    return name


def register_and_print() -> Affects[None, Console | UserStorage]:
    name = yield from ask_for_name()
    user_joke = yield from register_user(name)
    yield from Console.write(f"Here's your welcome joke:\n{user_joke}")


def main() -> Affects[None, Console | UserStorage]:
    @catch
    def catch_error(
        then: Continuation[...], err: Exception
    ) -> Affects[None, Console]:
        yield from Console.write(f"Error! {err!r}, ignoring.\n")

    yield from handle(catch_error, register_and_print())


if __name__ == "__main__":
    asyncio.run(
        arun(
            handle(
                default_stdio_handler
                + test_user_mgmt_handler
                + async_http_handler
                + handle_get_joke,
                main()
            )
        )
    )
