import json
from typing import Any

from affective import Continuation, Raise, catch, handle, handler, Affects
from affective.std.files import Files
from tasklist.core.effects import TaskStore
from tasklist.core.model import Task


@handler(TaskStore.load_list)
def _handle_file_load_list(
    then: Continuation[[list[Task]]]
) -> Affects[Any, Files]:
    def h():
        @handler(Raise.error)
        def if_no_task_file(
            then: Continuation[...], err: Exception
        ) -> Affects[Any, Files]:
            yield from Files.write("tasks.txt", b"[]")
            return b"[]"
        tasks_data = yield from handle(if_no_task_file, Files.read("tasks.txt"))
        try:
            tasks_json = json.loads(tasks_data.decode("utf-8"))
        except Exception as exc:
            ret = yield from Raise.error(exc)
        else:
            ret = yield from then([Task(**task) for task in tasks_json])
        return ret
    return (yield from then(h))


@handler(TaskStore.store_list)
def _handle_file_store_list(
    then: Continuation[[None]],
    tasks: list[Task]
) -> Affects[Any, Files]:
    def h():
        tasks_data = json.dumps(
            [
                {"name": task.name, "status": task.status}
                for task in tasks
            ]
        ).encode("utf-8")
        yield from Files.write("tasks.txt", tasks_data)
        ret = yield from then(None)
        return ret
    return (yield from then(h))


file_task_store_handler = _handle_file_store_list + _handle_file_load_list
