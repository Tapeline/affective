from affective import Raise
from affective.std.stdio import Affects, Console
from affective.tweaks.errors import transform_exceptions
from tasklist.core.effects import TaskStore
from tasklist.core.model import Task
from tasklist.core.usecase import (
    add_a_task,
    list_my_tasks,
    remove_a_task,
    set_task_status,
)


@transform_exceptions
def add_command(command: str) -> Affects[
    None, Console | TaskStore | Raise[Exception]
]:
    yield from add_a_task(Task(command[1:], "not_done"))


@transform_exceptions
def list_command(_: str) -> Affects[
    None, Console | TaskStore | Raise[Exception]
]:
    tasks = yield from list_my_tasks()
    rendered = "\n".join(
        f"{i}.\t[{'x' if task.status == 'done' else ' '}] {task.name}"
        for i, task in enumerate(tasks)
    )
    yield from Console.write(rendered + "\n")


@transform_exceptions
def remove_command(command: str)-> Affects[
    None, Console | TaskStore | Raise[Exception]
]:
    yield from remove_a_task(int(command[1:]))


@transform_exceptions
def set_status_command(command: str)-> Affects[
    None, Console | TaskStore | Raise[Exception]
]:
    task_no, status = command.split("=", maxsplit=2)
    if status not in {"not_done", "done"}:
        yield from Raise.error(ValueError("Status invalid"))
    else:
        yield from set_task_status(int(task_no), status)
