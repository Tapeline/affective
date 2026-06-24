from dataclasses import dataclass
from collections.abc import Mapping, Sequence, Callable, Generator
from typing import Any, Annotated, Concatenate, Awaitable,cast
from affective.core.types import Affects, Perform
from affective.core.handlers import OperationHandler, OperationHandlerCollection
from functools import wraps

class _MakeStatic[T]:
    # This is some black magic by mypy & Gemini
    # Helper annotation to trick mypy into thinking
    # that the method is static and doesn't need 
    # "self" as the first argument.
    def __get__(self, instance: Any, owner: type | None = None) -> T:
        raise NotImplementedError


def operation[**P, R](
    f: Callable[P, Affects[R]]
) -> _MakeStatic[
    Callable[P, Generator[Perform, Any, R]]
]:
    """
    Makes a method an operation.

    Args:
        f: target method

    Returns:
        a function that yields Perform of this operation

    """
    @wraps(f)
    def wrapper(
        *args: P.args, **kwargs: P.kwargs
    ) -> Generator[Perform, R | Perform, R]:
        ret = yield Perform(wrapper, args, kwargs), None
        return cast(R, ret)

    return wrapper  # type: ignore


def raw_handler[**P, R, SendT](
    eff_op: Callable[P, Generator[Perform, SendT, R]]
) -> Callable[
    [
        Callable[
            Concatenate[Callable[[R], Generator[Any, Any, Any]], P],
            Generator[Perform, SendT, R]
        ]
    ],
    OperationHandler
]:
    """
    Raw handler for an effect operation.

    Exposes k() API for the handler to be able to manually
    control the resumption of the continuation.
    The hanlder hence should end with:
    `return (yield from k(...))`

    """
    def wrapper(
        function: Callable[
            Concatenate[Callable[[R], Generator[Any, Any, Any]], P],
            Generator[Perform, SendT, R]
        ]
    ) -> OperationHandlerCollection:
        return OperationHandlerCollection({eff_op: function})

    return wrapper


def handler[**P, R, SendT](
    eff_op: Callable[P, Generator[Perform, SendT, R]]
) -> Callable[
    [Callable[P, Generator[Perform, SendT, R]]],
    OperationHandler
]:
    """
    Simple handler for an effect operation.

    Does not expose a raw continuation API.
    This handler can yield effects, but it cannot control
    the resumption: continuation always resumes exactly once
    and right after the handler has finished the work with
    the return value of the handler.

    """
    def wrapper(
        function: Callable[P, Generator[Perform, SendT, R]]
    ) -> OperationHandlerCollection:
        @raw_handler(eff_op)
        def raw_handle_func(
            k: Callable[[R], Generator[Any, Any, Any]], 
            *args: P.args, **kwargs: P.kwargs
        ):
            # breakpoint()
            res = function(*args, **kwargs)
            if hasattr(res, "__iter__"):
                res = yield from res
            return (yield from k(res))
        return raw_handle_func

    return wrapper


def catch[
    R,
    ThenContT: Callable[..., Any]
](
    on_catch: Callable[[ThenContT, Exception], Generator[Any, Any, Any]]
) -> OperationHandler:
    from affective.core.effects import Raise
    @raw_handler(Raise.error)  # type: ignore
    def _handler(
        cont: ThenContT, exc: Exception
    ) -> Generator[Perform, R, R]:
        ret: R = yield from on_catch(cont, exc)
        return ret

    return _handler
