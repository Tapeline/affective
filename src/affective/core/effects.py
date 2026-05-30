from collections.abc import Generator, Callable
from dataclasses import dataclass
from functools import wraps
from typing import (
    Annotated, Any, Sequence,
    Mapping,
)


@dataclass
class Perform:
    effect_type: Any
    effect_args: Sequence[Any]
    effect_kwargs: Mapping[str, Any]


class Effect:
    ...


class _StaticGeneratorMethod[T]:
    # This is some black magic by mypy & Gemini
    def __get__(self, instance: Any, owner: type | None = None) -> T:
        raise NotImplementedError


def operation[**P, R](f: Callable[P, R]) -> _StaticGeneratorMethod[
    Callable[P, Generator[Perform, Any, R]]
]:
    @wraps(f)
    def wrapper(
        *args: P.args, **kwargs: P.kwargs
    ) -> Generator[Perform, R, R]:
        ret = yield Perform(wrapper, args, kwargs)
        return ret

    return wrapper  # type: ignore


class Raise[ExcT: Exception](Effect):
    @operation
    def error[_ExcT: Exception](err: _ExcT) -> None: ...


type Affects[ReturnT, Effects = None] = Annotated[
    Generator[Perform, Any, ReturnT], Effects
]
