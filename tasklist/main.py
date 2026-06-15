from typing import Any

from affective import Continuation, Raise, catch, handle, handler, run
from affective.std.files import Files, default_files_handler
from affective.std.stdio import Console, Affects, default_stdio_handler
from tasklist.core.effects import TaskStore
from tasklist.core.model import Task
from tasklist.core.usecase import (
    add_a_task,
    list_my_tasks,
    remove_a_task,
    set_task_status,
)
from tasklist.shell.file_task_store import file_task_store_handler


def ask_command() -> Affects[str, Console]:
    yield from Console.write("> ")
    cmd = yield from Console.read()
    return cmd


def console_loop() -> Affects[None, Console | TaskStore | Raise[Exception]]:
    while True:
        command = yield from ask_command()
        if command.startswith("+"):
            yield from add_a_task(Task(command[1:], "not_done"))
        elif command == "l":
            tasks = yield from list_my_tasks()
            rendered = "\n".join(
                f"{i}.\t[{'x' if task.status == 'done' else ' '}] {task.name}"
                for i, task in enumerate(tasks)
            )
            yield from Console.write(rendered + "\n")
        elif command.startswith("-"):
            try:
                yield from remove_a_task(int(command[1:]))
            except ValueError as exc:
                yield from Raise.error(exc)
        elif "=" in command:
            task_no, status = command.split("=", maxsplit=2)
            if status not in {"not_done", "done"}:
                yield from Raise.error(ValueError("Status invalid"))
            else:
                yield from set_task_status(int(task_no), status)
        elif command == "q":
            break
        else:
            yield from Console.write("Unknown command\n")


def main() -> Affects[None, Console | TaskStore]:
    @handler(Raise.error)
    def on_console_error(
        then: Continuation[...], exc: Exception
    ) -> Affects[Any, Console]:
        def h():
            yield from Console.write(f"Error: {exc}\n")
            ret = yield from then(None)
            return ret
        return (yield from then(h))

    yield from handle(on_console_error, Files.read("test"))


if __name__ == "__main__":
    run(
        handle(
            default_stdio_handler
            + default_files_handler
            + file_task_store_handler,
            main()
        )
    )
