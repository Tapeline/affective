from collections.abc import Generator, Iterator, Callable
from dataclasses import dataclass
from functools import wraps
from typing import Annotated, Any, dataclass_transform, Self, Sequence, Mapping


@dataclass
class Perform:
    effect_type: Any
    effect_args: Sequence[Any]
    effect_kwargs: Mapping[str, Any]


class Effect:
    ...


def operation[**P, R](f: Callable[P, R]) -> Callable[
    P, Generator[Perform, Any, Any]
]:
    @wraps(f)
    def wrapper(
        *args: P.args, **kwargs: P.kwargs
    ) -> Generator[Perform, R, R]:
        ret = yield Perform(wrapper, args, kwargs)
        return ret

    return wrapper


def errors(
    *error_types: type[Exception],
) -> Callable[
    [Callable[..., Any]],
    Callable[..., Any],
]:
    def decorator[F: Callable[..., Any]](f: F) -> F:
        existing: tuple[type[Exception], ...] = getattr(
            f, "__affective_errors__", ()
        )
        setattr(f, "__affective_errors__", existing + error_types)
        return f

    return decorator


def get_errors(op: Callable[..., Any]) -> tuple[type[Exception], ...]:
    return getattr(op, "__affective_errors__", ())


class Raise[ExcT: Exception](Effect):
    @staticmethod
    @operation
    def error(err: ExcT) -> None: ...


type Affects[ReturnT, Effects] = Annotated[
    Generator[Perform, Any, ReturnT], Effects
]
