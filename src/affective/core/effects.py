from collections.abc import Generator, Callable
from dataclasses import dataclass
from functools import wraps
from typing import (
    Annotated, Any, Awaitable, Sequence,
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


@dataclass
class ImplicitRaise:
    exc: Exception


def operation[**P, R](f: Callable[P, R]) -> _StaticGeneratorMethod[
    Callable[P, Generator[Perform, Any, R]]
]:
    @wraps(f)
    def wrapper(
        *args: P.args, **kwargs: P.kwargs
    ) -> Generator[Perform, R, R]:
        ret = yield Perform(wrapper, args, kwargs)
        if ret.__class__ is ImplicitRaise:
            yield from Raise.error(ret.exc)
        return ret

    return wrapper  # type: ignore


class Raise[ExcT: Exception](Effect):
    @operation
    def error[_ExcT: Exception](err: _ExcT) -> None: ...


class Async(Effect):
    @operation
    def wait[T](coro: Awaitable[T]) -> T: ...


type Affects[ReturnT, Effects = None] = Annotated[
    Generator[Perform, Any, ReturnT], Effects
]
