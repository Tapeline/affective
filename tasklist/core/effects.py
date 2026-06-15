from affective import Effect, operation, Affects
from tasklist.core.model import Task


class TaskStore(Effect):
    @operation
    def store_list(tasks: list[Task]) -> Affects[None]: ...
    @operation
    def load_list() -> Affects[list[Task]]: ...
