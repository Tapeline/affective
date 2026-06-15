from dataclasses import dataclass
from typing import Literal, final, TypeAlias


TaskStatus: TypeAlias = Literal["done", "not_done"]


@dataclass
@final
class Task:
    name: str
    status: TaskStatus
