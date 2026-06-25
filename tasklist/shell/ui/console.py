from typing import Any

from affective import Raise, handle, Continue
from affective.std.stdio import Console, Affects
from tasklist.core.effects import TaskStore
from tasklist.shell.ui.commands import (
    add_command,
    list_command,
    remove_command, set_status_command,
)


def ask_command() -> Affects[str, Console]:
    yield from Console.write("> ")
    cmd = yield from Console.read()
    return cmd


def console_loop() -> Affects[None, Console | TaskStore | Raise[Exception]]:
    while True:
        command = yield from ask_command()
        if command.startswith("+"):
            yield from add_command(command)
        elif command == "l":
            yield from list_command(command)
        elif command.startswith("-"):
            yield from remove_command(command)
        elif "=" in command:
            yield from set_status_command(command)
        elif command == "q":
            break
        else:
            yield from Console.write("Unknown command\n")


def run_console() -> Affects[None, Console | TaskStore]:
    def continue_on_error(
        then: Continue[None], exc: Exception
    ) -> Affects[Any, Console]:
        yield from Console.write(f"Error: {exc}\n")
        return (yield from then(None))

    yield from handle(
        console_loop(),
        {Raise.error: continue_on_error}
    )
