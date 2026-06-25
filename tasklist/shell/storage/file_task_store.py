import json
from typing import Any

from affective import Raise, handle, handler, Affects, Continue
from affective.std.files import Files
from affective.tweaks.errors import try_or_raise

from tasklist.core.effects import TaskStore
from tasklist.core.model import Task


@handler(TaskStore.load_list)
def _handle_file_load_list() -> Affects[list[Task], Files | Raise[Exception]]:
    def if_no_task_file(
        then: Continue[None], _: Exception
    ) -> Affects[bytes, Files]:
        yield from Files.write("tasks.txt", b"[]")
        return (yield from then(None))

    tasks_data = yield from handle(
        Files.read("tasks.txt"),
        {Raise.error: if_no_task_file}
    )
    tasks_data = tasks_data or b"[]"

    task_json = yield from try_or_raise(
        lambda: json.loads(tasks_data.decode("utf-8")),
        fallback=[],
    )

    return [Task(**task) for task in task_json]


@handler(TaskStore.store_list)
def _handle_file_store_list(tasks: list[Task]) -> Affects[None, Files]:
    tasks_data = json.dumps(
        [
            {"name": task.name, "status": task.status}
            for task in tasks
        ]
    ).encode("utf-8")
    yield from Files.write("tasks.txt", tasks_data)


file_task_store_handler = _handle_file_store_list | _handle_file_load_list
