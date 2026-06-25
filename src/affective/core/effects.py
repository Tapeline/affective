from affective.core.types import Affects
from affective.core.decorators import operation
from typing import Awaitable


class Effect: ...


class Raise[ExcT: Exception](Effect):
    """Denotes an ability to throw a specific error."""
    @operation
    def error[_ExcT: Exception](err: _ExcT) -> Affects[None]:
        """Raise an exception in an effectful manner."""


class Async(Effect):
    """Denotes an ability to run and wait for coroutines"""
    @operation
    def wait[T](coro: Awaitable[T]) -> Affects[T, Raise[Exception]]:
        """
        Wait for a coroutine to finish.

        Because of an unsafe nature of exceptions,
        we can never guarantee, that the coroutine will
        not result in one, hence Async.wait always has
        a Raise[Exception] side effect.

        """
