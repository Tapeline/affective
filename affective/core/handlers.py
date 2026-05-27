from collections.abc import Callable, Generator
from dataclasses import dataclass
from functools import wraps
from typing import Any, Concatenate

from affective import Raise
from affective.core.effects import Perform
from affective.core.continuation import Continuation


@dataclass
class OperationHandlerCollection:
    handlers: dict[Any, Callable[
        Concatenate[Callable[[Any], Continuation], Any],
        Generator[Perform, Any, Any]
    ]]

    def __add__(
        self, other: Any
    ) -> "OperationHandlerCollection":
        match other:
            case OperationHandler(op, func):
                return OperationHandlerCollection(self.handlers | {op: func})
            case OperationHandlerCollection(handlers):
                return OperationHandlerCollection(handlers | self.handlers)
            case _:
                return NotImplemented

    def __radd__(self, other: Any) -> "OperationHandlerCollection":
        return self.__add__(other)


@dataclass
class OperationHandler[**P = ..., R = Any]:
    operation: Any
    func: Callable[
        Concatenate[Callable[[R], Continuation], P],
        Generator[Perform, Any, R]
    ]

    def __add__(self, other: Any) -> "OperationHandlerCollection":
        match other:
            case OperationHandler(op, func):
                return OperationHandlerCollection(
                    {op: func, self.operation: self.func}
                )
            case _:
                return NotImplemented


def handler[**P, R](
    eff_op: Callable[P, Generator[Perform, Any, R]]
) -> Callable[
    [
        Callable[
            Concatenate[Callable[[R], Continuation], P],
            Generator[Perform, Any, R]
        ]
    ],
    OperationHandler
]:
    def wrapper(
        function: Callable[
            Concatenate[Callable[[R], Continuation], P],
            Generator[Perform, Any, R]
        ]
    ) -> OperationHandler:
        return OperationHandler(eff_op, function)

    return wrapper


def catch(
    on_catch: Callable[
        [
            Callable[[], Continuation],
            Exception
        ], Continuation
    ]
) -> OperationHandler:
    @handler(Raise.error)
    def _handler(cont: Callable[[], Continuation], exc: Exception) -> Continuation:
        ret = yield from on_catch(cont, exc)
        return ret

    return _handler
