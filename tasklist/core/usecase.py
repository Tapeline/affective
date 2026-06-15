from dataclasses import replace

from affective import Affects
from tasklist.core.effects import TaskStore
from tasklist.core.model import Task, TaskStatus


def list_my_tasks() -> Affects[list[Task], TaskStore]:
    my_tasks = yield from TaskStore.load_list()
    return my_tasks


def add_a_task(task: Task) -> Affects[None, TaskStore]:
    my_tasks = yield from TaskStore.load_list()
    yield from TaskStore.store_list(my_tasks + [task])


def remove_a_task(index: int) -> Affects[None, TaskStore]:
    my_tasks = yield from TaskStore.load_list()
    my_tasks.pop(index)
    yield from TaskStore.store_list(my_tasks)


def set_task_status(
    index: int, new_status: TaskStatus
) -> Affects[None, TaskStore]:
    my_tasks = yield from TaskStore.load_list()
    my_tasks[index] = replace(my_tasks[index], status=new_status)
    yield from TaskStore.store_list(my_tasks)
