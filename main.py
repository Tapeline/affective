from affective import run, handle, Handler
from affective.std.stdio import (
    ReadStdin, WriteStdin, default_stdio_handler,
)
from sample_app.app.usecase import register_user
from sample_app.handlers.user_mgmt import test_user_mgmt_handler


def ask_for_name():
    yield WriteStdin("What is your name? ")
    name = yield ReadStdin()
    return name


def main():
    name = yield from ask_for_name()
    yield from register_user(name)


if __name__ == "__main__":
    h = handle(
            Handler(default_stdio_handler, test_user_mgmt_handler),
            main(),
        )
    run(
        h
    )
