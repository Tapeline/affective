from collections.abc import Callable, Generator
from dataclasses import dataclass
from typing import Any, Concatenate

from affective import Raise
from affective.core.effects import Perform
from affective.core.continuation import Continuation


@dataclass
class OperationHandlerCollection:
    handlers: dict[Any, Callable[
        ...,
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
        Concatenate[Continuation[[R]], P],
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
            Concatenate[Continuation[[R]], P],
            Generator[Perform, Any, R]
        ]
    ],
    OperationHandler
]:
    def wrapper(
        function: Callable[
            Concatenate[Continuation[[R]], P],
            Generator[Perform, Any, R]
        ]
    ) -> OperationHandler:
        return OperationHandler(eff_op, function)

    return wrapper


def catch[
    R,
    ThenContT: Continuation[...]
](
    on_catch: Continuation[[ThenContT, Exception]]
) -> OperationHandler:
    @handler(Raise.error)  # type: ignore
    def _handler(
        cont: ThenContT, exc: Exception
    ) -> Generator[Perform, R, R]:
        ret: R = yield from on_catch(cont, exc)
        return ret

    return _handler
