from collections.abc import Callable
from functools import wraps
from typing import Any

from affective.core.types import (
    Affects,
    Perform,
    EffectGen,
    Handler,
)


class _MakeStatic[T]:
    # This is some black magic by mypy & Gemini
    # Helper annotation to trick mypy into thinking
    # that the method is static and doesn't need 
    # "self" as the first argument.
    def __get__(self, instance: Any, owner: type | None = None) -> T:
        raise NotImplementedError


def operation[**P, R](
    f: Callable[P, Affects[R]]
) -> _MakeStatic[Callable[P, EffectGen[R]]]:
    """
    Makes a method an operation.

    Args:
        f: target method

    Returns:
        a function that yields Perform of this operation

    """

    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> EffectGen[R]:
        return (yield Perform(wrapper, args, kwargs), {})

    return wrapper  # type: ignore


def handler[**P, R](
    eff_op: Callable[P, EffectGen[R]]
) -> Callable[[Callable[P, EffectGen[R]]], Handler]:
    """
    Simple handler for an effect operation.

    Does not expose a raw continuation API.
    This handler can yield effects, but it cannot control
    the resumption: continuation always resumes exactly once
    and right after the handler has finished the work with
    the return value of the handler.

    """

    def wrapper(function: Callable[P, EffectGen[R]]) -> Handler:
        def raw_handle_func(
            k: Callable[[R], EffectGen[Any]],
            *args: P.args, **kwargs: P.kwargs
        ):
            res = yield from function(*args, **kwargs)
            return (yield from k(res))

        return {eff_op: raw_handle_func}

    return wrapper


def const_handler[**P, R](
    eff_op: Callable[P, EffectGen[R]]
) -> Callable[[Callable[P, R]], Handler]:
    """
    Simplest handler for an effect operation.

    Does not expose a raw continuation API, neither allows
    to yield effects.

    Should be used for yielding values or implementing low-level
    effects using the imperative API of Python or other libraries.
    Continuation always resumes exactly once
    and right after the handler has finished the work with
    the return value of the handler.

    """

    def wrapper(function: Callable[P, R]) -> Handler:
        def raw_handle_func(
            k: Callable[[R], EffectGen[Any]],
            *args: P.args, **kwargs: P.kwargs
        ):
            return (yield from k(function(*args, **kwargs)))

        return {eff_op: raw_handle_func}

    return wrapper