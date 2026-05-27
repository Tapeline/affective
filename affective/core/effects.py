from collections.abc import Generator, Iterator
from dataclasses import dataclass
from typing import Any, dataclass_transform, Self


@dataclass_transform(frozen_default=True)
def effect[E](cls: type[E]) -> type[E]:
    return dataclass(frozen=True, slots=True)(cls)


class Effect[ResultT]:
    ...


@effect
class Yield(Effect[None]): ...


@effect
class Raise[ExcT: Exception](Effect[None]):
    error: ExcT


def perform[ResultT](effect: Effect[ResultT]) -> Iterator[Effect[ResultT]]:
    return_value = yield effect
    return return_value
